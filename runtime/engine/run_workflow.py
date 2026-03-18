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
    statuses = set()

    for condition in termination_conditions:
        status = condition.get("status")
        if status:
            statuses.add(status)

    return statuses


def run_workflow(task: dict) -> None:
    workflow_name = task.get("workflow", "feature_development")
    workflow = load_workflow(workflow_name)

    start_role = workflow["start_role"]
    allowed_roles = workflow["allowed_roles"]
    termination_statuses = get_termination_statuses(workflow)

    print(f"\nStarting workflow: {workflow_name}")

    runs_dir = Path("runtime/runs")
    runs_dir.mkdir(parents=True, exist_ok=True)

    save_json(runs_dir / "current_task.json", task)

    current_role = start_role
    previous_output = None
    transition_counts: Dict[Tuple[str, str], int] = {}

    for step in range(1, MAX_WORKFLOW_STEPS + 1):
        validate_role(current_role, workflow_name, allowed_roles)

        print(f"\nRunning step {step}: {current_role}")

        result = run_agent_step(
            current_role,
            task,
            previous_output=previous_output,
        )

        # Execute file operations if provided
        file_operations = result.get("file_operations", [])
        execution_results = []

        if file_operations:
            print(f"Applying {len(file_operations)} file operation(s)...")
            execution_results = apply_file_operations(file_operations)
            result["execution_results"] = execution_results
            print("File operations applied.")

        step_file = runs_dir / f"step_{step:02d}_{current_role}.json"
        save_json(step_file, result)
        print(f"Saved step output: {step_file}")

        agent = result.get("agent")
        status = result.get("status")
        workflow_outcome = result.get("workflow_outcome")
        handoff = result.get("handoff", {})
        next_owner = handoff.get("next_owner")

        if agent != current_role:
            raise ValueError(
                f"Step {step} returned mismatched agent. "
                f"Expected '{current_role}', got '{agent}'."
            )

        if workflow_outcome == "completed" or status == "completed":
            print(f"\nWorkflow completed by {current_role}")
            return

        if workflow_outcome == "blocked" or status == "blocked":
            print(f"\nWorkflow blocked at {current_role}")
            return

        if status in termination_statuses:
            print(f"\nWorkflow stopped with terminal status: {status}")
            return

        if status not in ["ready for next stage", "requires revision"]:
            raise ValueError(
                f"Unsupported status returned at step {step}: {status}"
            )

        if not next_owner:
            raise ValueError(
                f"Step {step} ({current_role}) returned no handoff.next_owner"
            )

        validate_role(next_owner, workflow_name, allowed_roles)

        if status == "ready for next stage" and next_owner == current_role:
            raise RuntimeError(
                f"Invalid self-handoff at step {step}: "
                f"'{current_role}' cannot hand off to itself while continuing."
            )

        transition = (current_role, next_owner)
        transition_counts[transition] = transition_counts.get(transition, 0) + 1

        if transition_counts[transition] > MAX_TRANSITION_REPEATS:
            raise RuntimeError(
                f"Detected repeated workflow transition {current_role} -> {next_owner}. "
                f"This usually means the handoff chain is looping."
            )

        if status == "requires revision":
            print(
                f"\nRevision requested by {current_role}. "
                f"Routing to {next_owner} for corrective action."
            )

        previous_output = result
        current_role = next_owner

    raise RuntimeError(
        f"Workflow exceeded max step limit of {MAX_WORKFLOW_STEPS}. "
        "This usually means no agent is declaring completion or the handoff chain is looping."
    )