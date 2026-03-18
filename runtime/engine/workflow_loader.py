import yaml
from pathlib import Path


def load_workflow(workflow_name: str) -> dict:
    base = Path(__file__).resolve().parent.parent
    wf_path = base / "workflows" / f"{workflow_name}.yaml"

    if not wf_path.exists():
        raise ValueError(f"Workflow not found: {workflow_name}")

    with open(wf_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)