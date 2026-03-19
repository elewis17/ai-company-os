import json
import subprocess
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
RETRIEVER = BASE / "runtime/indexer/retrieve.py"
RETRIEVED = BASE / "runtime/indexer/retrieved_paths.json"
RUNS_DIR = BASE / "runtime/runs"

sys.path.append(str(BASE))

from runtime.engine.run_workflow import run_workflow  # noqa: E402


def select_workflow(paths: list[dict]) -> str:
    retrieved_paths = [p.get("path", "") for p in paths]

    if any(path.startswith("workflows/") for path in retrieved_paths):
        return "process_change"

    return "feature_development"


def load_latest_memory():
    """
    Load ONLY the latest QA feedback and artifacts.
    This creates a tight self-correction loop.
    """
    qa_file = RUNS_DIR / "step_04_qa_analyst.json"
    artifacts_file = RUNS_DIR / "step_03_artifacts.json"

    memory = {}

    if qa_file.exists():
        try:
            with open(qa_file, "r", encoding="utf-8") as f:
                memory["qa_feedback"] = json.load(f)
        except Exception:
            memory["qa_feedback"] = "Failed to load QA feedback"

    if artifacts_file.exists():
        try:
            with open(artifacts_file, "r", encoding="utf-8") as f:
                memory["artifact_bundle"] = json.load(f)
        except Exception:
            memory["artifact_bundle"] = "Failed to load artifacts"

    return memory


def augment_task_with_memory(task: dict) -> dict:
    memory = load_latest_memory()

    if not memory:
        return task

    # Inject into issue body (simple + effective)
    injection = "\n\n---\nPREVIOUS RUN CONTEXT\n"

    if "qa_feedback" in memory:
        injection += "\nQA FEEDBACK:\n"
        injection += json.dumps(memory["qa_feedback"], indent=2)

    if "artifact_bundle" in memory:
        injection += "\n\nARTIFACTS (LAST IMPLEMENTATION):\n"
        injection += json.dumps(memory["artifact_bundle"], indent=2)

    task["issue_body"] = (task.get("issue_body", "") + injection).strip()

    return task


# ----------- MAIN -----------

title = sys.argv[1]
body = sys.argv[2] if len(sys.argv) > 2 else ""

query = f"{title}\n{body}"

print("Running retriever...")

subprocess.run(
    ["python", str(RETRIEVER), query],
    check=True
)

print("Loading retrieved files...")

with open(RETRIEVED, "r", encoding="utf-8") as f:
    paths = json.load(f)

workflow_name = select_workflow(paths)

task = {
    "issue_title": title,
    "issue_body": body,
    "workflow": workflow_name,
    "retrieved_files": paths,
}

# 🔥 ADD MEMORY HERE
task = augment_task_with_memory(task)

print(f"Selected workflow: {workflow_name}")
print("Handing off to workflow engine...")

run_workflow(task)