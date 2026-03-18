import json
import subprocess
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
RETRIEVER = BASE / "runtime/indexer/retrieve.py"
RETRIEVED = BASE / "runtime/indexer/retrieved_paths.json"

sys.path.append(str(BASE))

from runtime.engine.run_workflow import run_workflow  # noqa: E402


def select_workflow(paths: list[dict]) -> str:
    retrieved_paths = [p.get("path", "") for p in paths]

    if any(path.startswith("workflows/") for path in retrieved_paths):
        return "process_change"

    return "feature_development"


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

print(f"Selected workflow: {workflow_name}")
print("Handing off to workflow engine...")

run_workflow(task)