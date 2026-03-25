import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

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


def _load_retrieved_paths(path: Path) -> List[dict]:
    if not path.exists():
        return []
    return json.loads(_read_text(path))


def _load_issue_metadata(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(_read_text(path))


def _extract_explicit_repo_paths(*texts: str) -> List[str]:
    pattern = re.compile(
        r"(?<![A-Za-z0-9_./-])((?:src|app|pages|components|features|runtime|scripts|public|supabase|\.github|tests?)/[^\s`'\"),:;]+|(?:package\.json|package-lock\.json|tsconfig(?:\.[^.\s/]+)?\.json|vite\.config\.[a-z]+|tailwind\.config\.[a-z]+|eslint\.config\.[a-z]+))(?![A-Za-z0-9_./-])"
    )
    found: List[str] = []
    seen = set()
    for text in texts:
        if not text:
            continue
        for match in pattern.findall(text):
            path = match.strip().strip("`\"'")
            if path and path not in seen:
                seen.add(path)
                found.append(path)
    return found


def _inject_explicit_target_files(retrieved_paths: List[dict], issue_metadata: Dict[str, Any]) -> List[dict]:
    title = str(issue_metadata.get("issue_title", "") or "")
    body = str(issue_metadata.get("issue_body", "") or "")
    explicit_paths = _extract_explicit_repo_paths(title, body)
    existing = {str(item.get("path", "")).strip() for item in retrieved_paths if isinstance(item, dict)}

    for path in explicit_paths:
        if path in existing:
            continue
        if Path(path).exists():
            retrieved_paths.append(
                {
                    "path": path,
                    "purpose": "target_repo_file",
                    "summary": "Explicitly referenced in the issue and injected as direct implementation context.",
                }
            )
    return retrieved_paths


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit("Usage: python scripts/run_task_packet.py <task_dir>")

    task_dir = Path(sys.argv[1]).resolve()
    task_file = task_dir / "task.md"
    retrieved_file = task_dir / "retrieved_paths.json"
    issue_metadata_file = task_dir / "issue_metadata.json"

    if not task_file.exists():
        raise FileNotFoundError(f"Task packet not found: {task_file}")

    task_text = _read_text(task_file)
    parsed = _parse_task_packet(task_text)
    issue_metadata = _load_issue_metadata(issue_metadata_file)
    retrieved_paths = _load_retrieved_paths(retrieved_file)
    retrieved_paths = _inject_explicit_target_files(retrieved_paths, issue_metadata or parsed)

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

    print("Injected target repo paths:", [item["path"] for item in retrieved_paths if item.get("purpose") == "target_repo_file"])

    run_with_bounded_retry(task)


if __name__ == "__main__":
    main()
