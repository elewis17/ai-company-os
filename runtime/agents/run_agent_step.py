import json
from typing import Any, Dict, Optional

from openai import OpenAI

from runtime.agents.agent_loader import load_agent_instructions
from runtime.config.roles import VALID_ROLES

client = OpenAI()


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
{json.dumps(previous_output, indent=2)}
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
                "file_operations": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "additionalProperties": False,
                        "properties": {
                            "action": {
                                "type": "string",
                                "enum": [
                                    "write_file",
                                    "append_file",
                                    "replace_in_file",
                                ],
                            },
                            "path": {
                                "type": "string",
                            },
                            "content": {
                                "type": "string",
                            },
                            "old": {
                                "type": "string",
                            },
                            "new": {
                                "type": "string",
                            },
                        },
                        "required": ["action", "path"],
                    },
                },
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
                    },
                    "required": ["instructions_loaded", "retrieved_file_count"],
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
{json.dumps(retrieved_files, indent=2)}

{previous_context}
You must follow the company's workflow handoff standard.

Runtime capabilities available now:
- The runner CAN apply file operations you return in "file_operations".
- Supported actions are:
  - write_file(path, content)
  - append_file(path, content)
  - replace_in_file(path, old, new)

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

6. If no repository changes are being proposed in this step:
   - execution_mode must be "planning" or "review"
   - file_operations must be []
   - artifacts_updated must be ["No repository artifacts updated in this stage"]

7. If you are software_engineer and the task is concrete enough to implement with the available file operations,
   you MUST switch to execution_mode = "implementation" and return the exact file_operations needed.
   Do not keep re-planning the same work.

8. If you return file_operations:
   - execution_mode must be "implementation"
   - artifacts_updated must list the exact target file paths
   - completed_work must describe the actual changes being applied
   - do not say a PR was opened, merged, or tests were run unless explicit executed tool results were provided

9. If the task is fully complete for the current workflow objective, set:
   - status = "completed"
   - workflow_outcome = "completed"
   - handoff.next_owner = "{agent_name}"
   - handoff.next_required_action = "No further action required"
   - next_required_action = "No further action required"

10. If the workflow cannot proceed because of a blocker, set:
   - status = "blocked"
   - workflow_outcome = "blocked"

11. If work should continue, set:
   - status = "ready for next stage"
   - workflow_outcome = "continue"

12. Do NOT create follow-up work inside the same workflow.
    If follow-up work is needed, mention it in blockers_or_risks or decision_or_outcome,
    but still mark the current task completed if its original objective is done.

13. If the workflow is "process_change", prefer routing among:
    technical_architect, project_manager, software_engineer, qa_analyst.
    Only route to product_manager if the task truly requires product-scope clarification.

14. For process_change workflows, prefer minimal documentation/process changes.
    Do not assume application feature implementation is required unless the task explicitly says so.

15. If status = "ready for next stage", handoff.next_owner must not be the same as the current agent.
    Self-handoffs are only allowed when the task is completed or blocked.

16. If the work has already been fully planned and there is no new decision, review finding, or implementation to add,
    mark the task "completed" instead of repeating the same handoff.

17. For implementation tasks, keep changes minimal and precise.
    Prefer one or a few exact file operations over broad speculative edits.

18. Base your recommendations only on:
    - the task
    - retrieved knowledge
    - prior handoff if provided
    Clearly label assumptions as assumptions.

Return only schema-compliant JSON.
"""

    response = client.chat.completions.create(
        model="gpt-5",
        response_format={
            "type": "json_schema",
            "json_schema": agent_output_schema,
        },
        messages=[
            {
                "role": "developer",
                "content": (
                    "You are a precise role-based engineering agent. "
                    "Obey role boundaries, use only canonical role IDs, "
                    "do not fabricate execution, and when repository changes are concrete "
                    "return exact file_operations for the runner to apply."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )

    content = response.choices[0].message.content
    if not content:
        raise ValueError("Agent returned empty content.")

    return json.loads(content)