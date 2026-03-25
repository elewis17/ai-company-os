import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, Optional

BASE = Path(__file__).resolve().parent.parent
RETRIEVER = BASE / "runtime/indexer/retrieve.py"
RETRIEVED = BASE / "runtime/indexer/retrieved_paths.json"
RUNS_DIR = BASE / "runtime/runs"

sys.path.append(str(BASE))

from runtime.engine.run_workflow import run_workflow  # noqa: E402

MAX_AUTO_RETRIES = 1


def select_workflow(paths: list[dict]) -> str:
    retrieved_paths = [p.get("path", "") for p in paths]

    if any(path.startswith("workflows/") for path in retrieved_paths):
        return "process_change"

    return "feature_development"


def _safe_load_json(path: Path) -> Optional[Dict[str, Any]]:
    if not path.exists():
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def _get_step_number(path: Path) -> int:
    try:
        return int(path.stem.split("_")[1])
    except Exception:
        return -1


def _find_latest(pattern: str) -> Optional[Path]:
    matches = list(RUNS_DIR.glob(pattern))
    if not matches:
        return None
    matches.sort(key=_get_step_number, reverse=True)
    return matches[0]


def _get_latest_qa_file() -> Optional[Path]:
    return _find_latest("step_*_qa_analyst.json")


def _get_latest_artifact_file() -> Optional[Path]:
    return _find_latest("step_*_artifacts.json")


def _latest_run_context() -> Dict[str, Any]:
    memory: Dict[str, Any] = {}

    qa_file = _get_latest_qa_file()
    artifact_file = _get_latest_artifact_file()

    if qa_file:
        qa_payload = _safe_load_json(qa_file)
        if qa_payload is not None:
            memory["qa_feedback"] = qa_payload
            memory["qa_feedback_file"] = str(qa_file)

    if artifact_file:
        artifact_payload = _safe_load_json(artifact_file)
        if artifact_payload is not None:
            memory["artifact_bundle"] = artifact_payload
            memory["artifact_bundle_file"] = str(artifact_file)

    return memory


def augment_task_with_memory(task: dict) -> dict:
    memory = _latest_run_context()

    if not memory:
        return task

    injection = "\n\n---\nPREVIOUS RUN CONTEXT\n"

    if "qa_feedback" in memory:
        injection += "\nQA FEEDBACK:\n"
        injection += json.dumps(memory["qa_feedback"], indent=2)

    if "artifact_bundle" in memory:
        injection += "\n\nARTIFACT BUNDLE:\n"
        injection += json.dumps(memory["artifact_bundle"], indent=2)

    task["issue_body"] = (task.get("issue_body", "") + injection).strip()
    return task


def _qa_status_requires_retry(qa_payload: Optional[Dict[str, Any]]) -> bool:
    if not qa_payload:
        return False
    return qa_payload.get("status") == "requires revision"


def _qa_status_terminal(qa_payload: Optional[Dict[str, Any]]) -> bool:
    if not qa_payload:
        return False
    status = qa_payload.get("status")
    workflow_outcome = qa_payload.get("workflow_outcome")
    return (
        status in {"completed", "blocked"}
        or workflow_outcome in {"completed", "blocked"}
    )


def _artifact_has_changed_files(artifact_payload: Optional[Dict[str, Any]]) -> bool:
    if not artifact_payload:
        return False

    files = artifact_payload.get("files", [])
    if not isinstance(files, list) or not files:
        return False

    for item in files:
        if isinstance(item, dict) and item.get("path"):
            return True

    return False


def _build_retry_task(base_task: dict) -> dict:
    retry_task = dict(base_task)
    return augment_task_with_memory(retry_task)


def _run_initial_workflow(task: dict) -> None:
    run_workflow(task)


def _run_retry_slice(task: dict) -> None:
    run_workflow(
        task,
        start_role_override="software_engineer",
        max_steps_override=2,
    )


def run_with_bounded_retry(task: dict) -> None:
    RUNS_DIR.mkdir(parents=True, exist_ok=True)

    print(f"Selected workflow: {task['workflow']}")
    print("Handing off to workflow engine...")

    _run_initial_workflow(task)

    retries_used = 0

    while retries_used < MAX_AUTO_RETRIES:
        qa_file = _get_latest_qa_file()
        artifact_file = _get_latest_artifact_file()

        qa_payload = _safe_load_json(qa_file) if qa_file else None
        artifact_payload = _safe_load_json(artifact_file) if artifact_file else None

        if _qa_status_terminal(qa_payload):
            print("\nWorkflow reached terminal state. Stopping.")
            return

        if not _qa_status_requires_retry(qa_payload):
            print("\nNo retry needed. Stopping.")
            return

        if not _artifact_has_changed_files(artifact_payload):
            print("\nQA requested revision, but no changed-file artifact was found. Stopping.")
            return

        retries_used += 1
        print(f"\nAuto-retry triggered ({retries_used}/{MAX_AUTO_RETRIES})")
        print("Re-running corrective slice: software_engineer -> qa_analyst")

        retry_task = _build_retry_task(task)
        _run_retry_slice(retry_task)

        qa_file = _get_latest_qa_file()
        qa_payload = _safe_load_json(qa_file) if qa_file else None

        if _qa_status_terminal(qa_payload):
            print("\nWorkflow reached terminal state after retry. Stopping.")
            return

        if not _qa_status_requires_retry(qa_payload):
            print("\nRetry completed. No further retry needed.")
            return

    print("\nMax auto-retries reached. Stopping.")


def build_task_from_issue(title: str, body: str) -> dict:
    query = f"{title}\n{body}".strip()

    print("Running retriever...")
    subprocess.run(["python", str(RETRIEVER), query], check=True)

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

    return augment_task_with_memory(task)


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit("Usage: python scripts/run_agent.py <issue_title> [issue_body]")

    title = sys.argv[1]
    body = sys.argv[2] if len(sys.argv) > 2 else ""

    task = build_task_from_issue(title, body)
    run_with_bounded_retry(task)


if __name__ == "__main__":
    main()
