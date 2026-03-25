import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, Optional

BASE = Path(__file__).resolve().parent.parent
RUNS_DIR = BASE / "runtime/runs"

sys.path.append(str(BASE))

from scripts.run_agent import augment_task_with_memory, run_with_bounded_retry, select_workflow  # noqa: E402


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _extract(pattern: str, text: str) -> Optional[str]:
    match = re.search(pattern, text, re.MULTILINE)
    if not match:
        return None
    return match.group(1).strip()


def _parse_task_packet(task_text: str) -> Dict[str, Any]:
    issue_number = _extract(r"^Issue:\s*#(\d+)\s*$", task_text)
    title = _extract(r"^Title:\s*(.+)\s*$", task_text)

    description_match = re.search(
        r"^Description:\s*\n(.*?)\n---\s*\n\n# Retrieved OS Context",
        task_text,
        re.MULTILINE | re.DOTALL,
    )
    description = description_match.group(1).strip() if description_match else ""

    if not title:
        raise ValueError("Could not parse issue title from task packet")

    return {
        "issue_number": issue_number,
        "issue_title": title,
        "issue_body": description,
    }


def _load_retrieved_paths(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return json.loads(_read_text(path))


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit("Usage: python scripts/run_task_packet.py <task_dir>")

    task_dir = Path(sys.argv[1]).resolve()
    task_file = task_dir / "task.md"
    retrieved_file = task_dir / "retrieved_paths.json"

    if not task_file.exists():
        raise FileNotFoundError(f"Task packet not found: {task_file}")

    task_text = _read_text(task_file)
    parsed = _parse_task_packet(task_text)
    retrieved_paths = _load_retrieved_paths(retrieved_file)

    task: Dict[str, Any] = {
        "issue_title": parsed["issue_title"],
        "issue_body": parsed["issue_body"],
        "workflow": select_workflow(retrieved_paths),
        "retrieved_files": retrieved_paths,
    }

    if parsed.get("issue_number"):
        task["issue_number"] = parsed["issue_number"]

    task = augment_task_with_memory(task)

    RUNS_DIR.mkdir(parents=True, exist_ok=True)
    (RUNS_DIR / "current_task.json").write_text(json.dumps(task, indent=2), encoding="utf-8")

    run_with_bounded_retry(task)


if __name__ == "__main__":
    main()
