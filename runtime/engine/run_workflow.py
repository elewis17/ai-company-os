import json
from pathlib import Path
from typing import Dict, List, Tuple

from runtime.agents.run_agent_step import run_agent_step
from runtime.config.roles import VALID_ROLES
from runtime.engine.workflow_loader import load_workflow
from runtime.tools.execution_tools import apply_file_operations

MAX_WORKFLOW_STEPS = 12
MAX_TRANSITION_REPEATS = 2


def save_json(path: Path, payload: dict) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)


def validate_role(role: str, workflow_name: str, allowed_roles: List[str]) -> None:
    if role not in VALID_ROLES:
        raise ValueError(f"Invalid role returned by workflow: {role}")

    if role not in allowed_roles:
        raise ValueError(
            f"Role '{role}' is not allowed in workflow '{workflow_name}'"
        )


def get_termination_statuses(workflow: dict) -> set[str]:
    termination_conditions = workflow.get("termination_conditions", [])
    return {c.get("status") for c in termination_conditions if c.get("status")}


def build_changed_files_artifact(file_operations: List[dict]) -> dict:
    files = []
    for op in file_operations:
        path = op.get("path")
        action = op.get("action")

        if not path:
            continue

        path_obj = Path(path)
        content = None

        if path_obj.exists() and path_obj.is_file():
            try:
                content = path_obj.read_text(encoding="utf-8")
            except Exception:
                content = None

        files.append({
            "path": path,
            "action": action,
            "exists": path_obj.exists(),
            "content": content,
        })

    return {"files": files}


def run_workflow(task: dict, start_role_override=None, max_steps_override=None):
    workflow_name = task.get("workflow", "feature_development")
    workflow = load_workflow(workflow_name)

    start_role = workflow["start_role"]
    allowed_roles = workflow["allowed_roles"]
    termination_statuses = get_termination_statuses(workflow)

    print(f"\nStarting workflow: {workflow_name}")

    runs_dir = Path("runtime/runs")
    runs_dir.mkdir(parents=True, exist_ok=True)
    save_json(runs_dir / "current_task.json", task)

    current_role = start_role_override or start_role
    previous_output = None
    previous_role = None

    transition_counts: Dict[Tuple[str, str], int] = {}
    max_steps = max_steps_override or MAX_WORKFLOW_STEPS

    for step in range(1, max_steps + 1):
        validate_role(current_role, workflow_name, allowed_roles)

        print(f"\nRunning step {step}: {current_role}")

        result = run_agent_step(
            current_role,
            task,
            previous_output=previous_output,
        )

        file_operations = result.get("file_operations", [])

        if file_operations:
            if current_role != "software_engineer":
                raise ValueError("Only software_engineer can modify files")

            print(f"Applying {len(file_operations)} file operation(s)...")

            execution_results = apply_file_operations(file_operations)
            result["execution_results"] = execution_results

            artifact_bundle = build_changed_files_artifact(file_operations)
            artifact_path = runs_dir / f"step_{step:02d}_artifacts.json"

            save_json(artifact_path, artifact_bundle)

            result["artifact_bundle_file"] = str(artifact_path)
            result["artifact_bundle"] = artifact_bundle

            print(f"Artifacts saved: {artifact_path}")

        step_file = runs_dir / f"step_{step:02d}_{current_role}.json"
        save_json(step_file, result)

        agent = result.get("agent")
        status = result.get("status")
        workflow_outcome = result.get("workflow_outcome")
        handoff = result.get("handoff", {})
        next_owner = handoff.get("next_owner")

        if agent != current_role:
            raise ValueError("Agent mismatch")

        # ✅ TERMINATION (correct)
        if workflow_outcome == "completed" or status == "completed":
            print(f"\nWorkflow completed by {current_role}")
            return

        if workflow_outcome == "blocked" or status == "blocked":
            print(f"\nWorkflow blocked at {current_role}")
            return

        if status in termination_statuses:
            print(f"\nWorkflow stopped with terminal status: {status}")
            return

        if status == "requires revision":
            return

        if status != "ready for next stage":
            raise ValueError(f"Invalid status: {status}")

        if not next_owner:
            raise ValueError("Missing next_owner")

        validate_role(next_owner, workflow_name, allowed_roles)

        # 🔥 FIX: PM LOOP GUARD (THIS IS THE REAL FIX)
        if current_role == "project_manager":
            if previous_role == "software_engineer" and next_owner == "software_engineer":
                print("\nFixing PM loop → redirecting to QA instead of engineer")
                next_owner = "qa_analyst"
                result["handoff"]["next_owner"] = "qa_analyst"

        if next_owner == current_role:
            raise RuntimeError("Self handoff detected")

        transition = (current_role, next_owner)
        transition_counts[transition] = transition_counts.get(transition, 0) + 1

        if transition_counts[transition] > MAX_TRANSITION_REPEATS:
            raise RuntimeError(
                f"Detected repeated workflow transition {current_role} -> {next_owner}"
            )

        previous_output = result
        previous_role = current_role
        current_role = next_owner

    raise RuntimeError("Workflow exceeded max steps")