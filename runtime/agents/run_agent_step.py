import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

from openai import OpenAI

from runtime.agents.agent_loader import load_agent_instructions
from runtime.config.roles import VALID_ROLES

client = OpenAI()

RUNS_DIR = Path("runtime/runs")
MAX_INLINE_FILE_CHARS = 120000
IMPLEMENTATION_ROLE = "software_engineer"


def _safe_json_dumps(value: Any) -> str:
    return json.dumps(value, indent=2, ensure_ascii=True, allow_nan=False)


def _read_text_file(path_str: str) -> Optional[str]:
    path = Path(path_str)
    if not path.exists() or not path.is_file():
        return None
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")


def _truncate_text(text: str, max_chars: int = MAX_INLINE_FILE_CHARS) -> str:
    if len(text) <= max_chars:
        return text
    head = text[: max_chars // 2]
    tail = text[-(max_chars // 2) :]
    return (
        f"{head}\n\n"
        f"... [TRUNCATED FOR CONTEXT SIZE: original_length={len(text)} chars] ...\n\n"
        f"{tail}"
    )


def _extract_changed_paths(previous_output: Optional[Dict[str, Any]]) -> List[str]:
    if not previous_output:
        return []

    paths: List[str] = []

    for op in previous_output.get("file_operations", []) or []:
        path = op.get("path")
        if isinstance(path, str) and path.strip():
            paths.append(path.strip())

    for artifact in previous_output.get("artifacts_updated", []) or []:
        if (
            isinstance(artifact, str)
            and artifact.strip()
            and artifact != "No repository artifacts updated in this stage"
        ):
            paths.append(artifact.strip())

    seen: Set[str] = set()
    deduped: List[str] = []
    for path in paths:
        if path not in seen:
            seen.add(path)
            deduped.append(path)

    return deduped


def _extract_qa_issues(previous_output: Optional[Dict[str, Any]]) -> List[str]:
    if not previous_output:
        return []

    issues: List[str] = []

    for item in previous_output.get("blockers_or_risks", []) or []:
        if isinstance(item, str) and item.strip():
            issues.append(item.strip())

    for item in previous_output.get("decision_or_outcome", []) or []:
        if isinstance(item, str) and item.strip():
            text = item.strip()
            lowered = text.lower()
            if any(
                marker in lowered
                for marker in [
                    "fail",
                    "failed",
                    "failing",
                    "missing",
                    "incorrect",
                    "issue",
                    "problem",
                    "gap",
                    "needs revision",
                    "does not",
                    "not",
                ]
            ):
                issues.append(text)

    seen: Set[str] = set()
    deduped: List[str] = []
    for issue in issues:
        if issue not in seen:
            seen.add(issue)
            deduped.append(issue)

    return deduped


def _build_changed_files_bundle(previous_output: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    changed_paths = _extract_changed_paths(previous_output)

    files: List[Dict[str, Any]] = []
    for path_str in changed_paths:
        content = _read_text_file(path_str)
        path_obj = Path(path_str)
        files.append(
            {
                "path": path_str,
                "exists": path_obj.exists(),
                "size_bytes": path_obj.stat().st_size if path_obj.exists() and path_obj.is_file() else None,
                "content": _truncate_text(content) if content is not None else None,
            }
        )

    return {
        "changed_paths": changed_paths,
        "files": files,
    }


def _write_artifact_bundle(agent_name: str, bundle: Dict[str, Any]) -> Optional[str]:
    RUNS_DIR.mkdir(parents=True, exist_ok=True)
    artifact_path = RUNS_DIR / f"context_bundle_{agent_name}.json"
    artifact_path.write_text(_safe_json_dumps(bundle), encoding="utf-8")
    return str(artifact_path)


def _build_context_mode(
    agent_name: str,
    task: Dict[str, Any],
    previous_output: Optional[Dict[str, Any]],
    retrieved_files: List[Any],
) -> Dict[str, Any]:
    if agent_name == "qa_analyst":
        bundle = _build_changed_files_bundle(previous_output)
        artifact_file = _write_artifact_bundle(agent_name, bundle)
        return {
            "mode": "review_bundle",
            "description": (
                "Use exact changed files from the immediately prior step as the primary review source of truth."
            ),
            "artifact_bundle_file": artifact_file,
            "artifact_bundle": bundle,
        }

    if agent_name == IMPLEMENTATION_ROLE:
        target_paths: List[str] = []

        if previous_output:
            impl = previous_output.get("implementation_plan", {}) or {}
            for item in impl.get("recommended_first_changes", []) or []:
                if isinstance(item, str):
                    target_paths.append(item.strip())

        for path_str in _extract_changed_paths(previous_output):
            target_paths.append(path_str)

        for item in retrieved_files:
            if isinstance(item, dict):
                path = item.get("path")
                if isinstance(path, str) and path.strip():
                    target_paths.append(path.strip())

        seen: Set[str] = set()
        deduped_paths: List[str] = []
        for path in target_paths:
            if path and path not in seen and Path(path).exists():
                seen.add(path)
                deduped_paths.append(path)

        files: List[Dict[str, Any]] = []
        for path_str in deduped_paths[:10]:
            content = _read_text_file(path_str)
            files.append(
                {
                    "path": path_str,
                    "content": _truncate_text(content) if content is not None else None,
                }
            )

        bundle = {
            "qa_issues": _extract_qa_issues(previous_output),
            "target_paths": deduped_paths[:10],
            "files": files,
        }
        artifact_file = _write_artifact_bundle(agent_name, bundle)

        return {
            "mode": "targeted_file",
            "description": (
                "Use targeted file contents for implementation. Focus on files most likely to be edited. "
                "If QA issues are present from the previous step, prioritize fixing those issues with minimal changes."
            ),
            "artifact_bundle_file": artifact_file,
            "artifact_bundle": bundle,
        }

    return {
        "mode": "summary",
        "description": (
            "Use lightweight summary context only. Prefer retrieved summaries and prior handoff over full file text."
        ),
        "artifact_bundle_file": None,
        "artifact_bundle": None,
    }


FILE_OPERATION_SCHEMA: Dict[str, Any] = {
    "type": "array",
    "items": {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "action": {
                "type": "string",
                "enum": ["write_file", "append_file", "replace_in_file"],
            },
            "path": {
                "type": "string",
            },
            "content": {
                "type": ["string", "null"],
            },
            "old": {
                "type": ["string", "null"],
            },
            "new": {
                "type": ["string", "null"],
            },
        },
        "required": ["action", "path", "content", "old", "new"],
    },
}


def _default_non_implementation_mode(agent_name: str) -> str:
    if agent_name == "qa_analyst":
        return "review"
    return "planning"


def _enforce_role_execution_rules(agent_name: str, result: Dict[str, Any]) -> Dict[str, Any]:
    if agent_name == IMPLEMENTATION_ROLE:
        return result

    file_operations = result.get("file_operations") or []
    if not file_operations:
        if result.get("execution_mode") == "implementation":
            result["execution_mode"] = _default_non_implementation_mode(agent_name)
        return result

    result["file_operations"] = []
    result["execution_mode"] = _default_non_implementation_mode(agent_name)
    result["artifacts_updated"] = ["No repository artifacts updated in this stage"]

    completed_work = result.get("completed_work") or []
    result["completed_work"] = [
        item
        for item in completed_work
        if "file" not in item.lower() and "write" not in item.lower()
    ]

    decision_or_outcome = result.get("decision_or_outcome") or []
    decision_or_outcome.append(
        f"Non-implementation role '{agent_name}' proposed file operations; they were removed by runtime role enforcement."
    )
    result["decision_or_outcome"] = decision_or_outcome

    blockers_or_risks = result.get("blockers_or_risks") or []
    blockers_or_risks.append(
        f"Role boundary violation prevented: '{agent_name}' attempted repository mutation."
    )
    result["blockers_or_risks"] = blockers_or_risks

    return result


def run_agent_step(
    agent_name: str,
    task: Dict[str, Any],
    previous_output: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    instructions = load_agent_instructions(agent_name)
    retrieved_files = task.get("retrieved_files", [])
    workflow_name = task.get("workflow", "")

    previous_context = ""
    if previous_output is not None:
        previous_context = f"""
PREVIOUS STEP OUTPUT
{_safe_json_dumps(previous_output)}
"""

    context_mode = _build_context_mode(
        agent_name=agent_name,
        task=task,
        previous_output=previous_output,
        retrieved_files=retrieved_files,
    )

    artifact_context = ""
    if context_mode["artifact_bundle"] is not None:
        artifact_context = f"""

CONTEXT MODE
Mode: {context_mode["mode"]}
Description: {context_mode["description"]}
Artifact Bundle File: {context_mode["artifact_bundle_file"]}

ARTIFACT BUNDLE
{_safe_json_dumps(context_mode["artifact_bundle"])}
"""

    qa_fix_context = ""
    if agent_name == IMPLEMENTATION_ROLE:
        qa_issues = _extract_qa_issues(previous_output)
        if qa_issues:
            qa_fix_context = f"""

QA FIX PRIORITY
The previous step surfaced concrete QA issues. You must address these first with minimal, surgical changes.

QA ISSUES
{_safe_json_dumps(qa_issues)}
"""

    agent_output_schema = {
        "name": "agent_step_output",
        "strict": True,
        "schema": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "agent": {
                    "type": "string",
                    "enum": [agent_name],
                },
                "status": {
                    "type": "string",
                    "enum": [
                        "ready for next stage",
                        "blocked",
                        "requires revision",
                        "completed",
                    ],
                },
                "workflow_outcome": {
                    "type": "string",
                    "enum": [
                        "continue",
                        "completed",
                        "blocked",
                    ],
                },
                "execution_mode": {
                    "type": "string",
                    "enum": [
                        "planning",
                        "review",
                        "implementation",
                    ],
                },
                "summary": {
                    "type": "string",
                },
                "completed_work": {
                    "type": "array",
                    "items": {"type": "string"},
                },
                "artifacts_updated": {
                    "type": "array",
                    "items": {"type": "string"},
                },
                "decision_or_outcome": {
                    "type": "array",
                    "items": {"type": "string"},
                },
                "next_required_action": {
                    "type": "string",
                },
                "blockers_or_risks": {
                    "type": "array",
                    "items": {"type": "string"},
                },
                "implementation_plan": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "goal": {
                            "type": "string",
                        },
                        "issue_body": {
                            "type": "string",
                        },
                        "recommended_first_changes": {
                            "type": "array",
                            "items": {"type": "string"},
                        },
                        "notes": {
                            "type": "array",
                            "items": {"type": "string"},
                        },
                    },
                    "required": [
                        "goal",
                        "issue_body",
                        "recommended_first_changes",
                        "notes",
                    ],
                },
                "file_operations": FILE_OPERATION_SCHEMA,
                "handoff": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "next_owner": {
                            "type": "string",
                            "enum": VALID_ROLES,
                        },
                        "next_required_action": {
                            "type": "string",
                        },
                    },
                    "required": ["next_owner", "next_required_action"],
                },
                "debug": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "instructions_loaded": {
                            "type": "boolean",
                        },
                        "retrieved_file_count": {
                            "type": "integer",
                        },
                        "context_mode": {
                            "type": "string",
                            "enum": ["summary", "targeted_file", "review_bundle"],
                        },
                        "artifact_bundle_file": {
                            "type": ["string", "null"],
                        },
                    },
                    "required": [
                        "instructions_loaded",
                        "retrieved_file_count",
                        "context_mode",
                        "artifact_bundle_file",
                    ],
                },
            },
            "required": [
                "agent",
                "status",
                "workflow_outcome",
                "execution_mode",
                "summary",
                "completed_work",
                "artifacts_updated",
                "decision_or_outcome",
                "next_required_action",
                "blockers_or_risks",
                "implementation_plan",
                "file_operations",
                "handoff",
                "debug",
            ],
        },
    }

    prompt = f"""
You are executing the role: {agent_name}.

ROLE INSTRUCTIONS
{instructions}

TASK
Title: {task.get("issue_title", "")}
Body: {task.get("issue_body", "")}
Workflow: {workflow_name}

RETRIEVED KNOWLEDGE
{_safe_json_dumps(retrieved_files)}

{previous_context}
{artifact_context}
{qa_fix_context}

You must follow the company's workflow handoff standard.

Runtime capabilities available now:
- The runner CAN apply file operations you return in "file_operations".
- Supported actions are:
  - write_file(path, content)
  - append_file(path, content)
  - replace_in_file(path, old, new)

Context strategy:
- technical_architect and project_manager should remain lightweight and summary-driven unless exact file text is required
- software_engineer should use targeted file contents when available
- qa_analyst must treat artifact bundle file contents as the primary source of truth for review

Rules:
1. Only use these valid next_owner roles exactly as written:
   {", ".join(VALID_ROLES)}

2. Do not invent new roles.

3. The "agent" field must be exactly "{agent_name}".

4. Respect role boundaries:
   - product_manager defines product scope and requirements
   - project_manager coordinates workflow/process execution and delivery
   - technical_architect protects architecture and standards
   - software_engineer implements approved technical work
   - qa_analyst validates quality and test sufficiency

5. Do not claim repository files were changed unless you are also returning the exact file_operations needed to make those changes.

6. Only {IMPLEMENTATION_ROLE} may return non-empty file_operations.
   All other roles must return file_operations = [].

7. Only {IMPLEMENTATION_ROLE} may use execution_mode = "implementation".
   - technical_architect must use "planning"
   - project_manager must use "planning"
   - product_manager must use "planning"
   - qa_analyst must use "review"
   - software_engineer may use "implementation" when making repository changes

8. If you are not {IMPLEMENTATION_ROLE}:
   - do not return file operations
   - do not describe code or file changes as completed
   - hand off implementation work to {IMPLEMENTATION_ROLE} when repository changes are needed

9. If no repository changes are being proposed in this step:
   - execution_mode must be "planning" or "review"
   - file_operations must be []
   - artifacts_updated must be ["No repository artifacts updated in this stage"]

10. If you are {IMPLEMENTATION_ROLE} and the task is concrete enough to implement with the available file operations,
    you MUST switch to execution_mode = "implementation" and return the exact file_operations needed.
    Do not keep re-planning the same work.

11. If you return file_operations:
    - execution_mode must be "implementation"
    - artifacts_updated must list the exact target file paths
    - completed_work must describe the actual changes being applied
    - do not say a PR was opened, merged, or tests were run unless explicit executed tool results were provided

12. If the task is fully complete for the current workflow objective, set:
    - status = "completed"
    - workflow_outcome = "completed"
    - handoff.next_owner = "{agent_name}"
    - handoff.next_required_action = "No further action required"
    - next_required_action = "No further action required"

13. If the workflow cannot proceed because of a blocker, set:
    - status = "blocked"
    - workflow_outcome = "blocked"

14. If work should continue, set:
    - status = "ready for next stage"
    - workflow_outcome = "continue"

15. Do NOT create follow-up work inside the same workflow.
    If follow-up work is needed, mention it in blockers_or_risks or decision_or_outcome,
    but still mark the current task completed if its original objective is done.

16. If the workflow is "process_change", prefer routing among:
    technical_architect, project_manager, software_engineer, qa_analyst.
    Only route to product_manager if the task truly requires product-scope clarification.

17. For process_change workflows, prefer minimal documentation/process changes.
    Do not assume application feature implementation is required unless the task explicitly says so.

18. If status = "ready for next stage", handoff.next_owner must not be the same as the current agent.
    Self-handoffs are only allowed when the task is completed or blocked.

19. If the work has already been fully planned and there is no new decision, review finding, or implementation to add,
    mark the task "completed" instead of repeating the same handoff.

20. For implementation tasks, keep changes minimal and precise.
    Prefer one or a few exact file operations over broad speculative edits.

21. Base your recommendations only on:
    - the task
    - retrieved knowledge
    - prior handoff if provided
    - artifact bundle contents if provided
    Clearly label assumptions as assumptions.

22. If you are qa_analyst and an artifact bundle is present:
    - review the actual changed file contents in the bundle
    - verify whether the change satisfies the stated purpose from the previous step
    - block only for concrete gaps you can point to in the changed files

23. If you are {IMPLEMENTATION_ROLE} and targeted files are present:
    - use those files as your main implementation context
    - keep edits narrowly scoped to the stated objective

24. If you are {IMPLEMENTATION_ROLE} and QA issues are present from the previous step:
    - treat those QA issues as the highest priority
    - make the smallest change set needed to fix them
    - do not broaden scope unless a QA issue explicitly requires it

25. If you are {IMPLEMENTATION_ROLE}:
    - return repository-ready file content only
    - never include prompt text, schema text, commentary, or explanation inside file content unless the file itself truly requires it
    - use write_file for new files or full-file rewrites
    - use replace_in_file when you have an exact, stable target block to replace
    - use append_file only when content truly belongs at the end of the file and there is no stable replacement anchor
    - prefer the smallest safe change that fully resolves the task or QA issue

26. File operation field rules:
    - every file operation must include: action, path, content, old, new
    - for write_file: set content to the final file text, and set old = null, new = null
    - for append_file: set content to the appended file text, and set old = null, new = null
    - for replace_in_file: set old and new to exact text values, and set content = null
    - do not use empty-string placeholders for unused fields unless the file content itself is intentionally empty

27. If you use replace_in_file:
    - old must be the exact text to replace
    - new must be the exact replacement text
    - do not shorten old/new to summaries or partial hints

28. If you use write_file or append_file:
    - content must be final file content only
    - do not wrap content in JSON, prose, or meta-instructions

Return only schema-compliant JSON.
"""

    payload = {
        "model": "gpt-5",
        "response_format": {
            "type": "json_schema",
            "json_schema": agent_output_schema,
        },
        "messages": [
            {
                "role": "developer",
                "content": (
                    "You are a precise role-based engineering agent. "
                    "Obey role boundaries, use only canonical role IDs, "
                    "do not fabricate execution, and when repository changes are concrete "
                    "return exact file_operations for the runner to apply. "
                    f"Only {IMPLEMENTATION_ROLE} may return non-empty file_operations or use execution_mode='implementation'. "
                    "All other roles must plan, review, or hand off. "
                    "For software_engineer tasks, return repository-ready file mutations only. "
                    "Never leak prompt text, schema text, or commentary into file content."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
    }

    RUNS_DIR.mkdir(parents=True, exist_ok=True)

    try:
        serialized = json.dumps(payload, ensure_ascii=False, allow_nan=False, indent=2)
        (RUNS_DIR / f"debug_payload_{agent_name}.json").write_text(serialized, encoding="utf-8")
    except Exception as e:
        raise ValueError(f"Payload failed local JSON serialization for {agent_name}: {e}")

    response = client.chat.completions.create(**payload)

    content = response.choices[0].message.content
    if not content:
        raise ValueError("Agent returned empty content.")

    result = json.loads(content)
    result = _enforce_role_execution_rules(agent_name, result)

    result["debug"]["context_mode"] = context_mode["mode"]
    result["debug"]["artifact_bundle_file"] = context_mode["artifact_bundle_file"]

    return result