from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import List


OS_REPO_ROOT = Path(__file__).resolve().parents[2]


def _resolve_target_repo_root() -> Path:
    configured_root = os.environ.get("LEASE_LENS_REPO_ROOT") or os.environ.get("TARGET_REPO_ROOT")
    base = Path(configured_root).expanduser().resolve() if configured_root else OS_REPO_ROOT

    if not base.exists() or not base.is_dir():
        raise ValueError(f"Configured repository root is invalid: {base}")

    return base


BASE = _resolve_target_repo_root()


@dataclass
class FileOperationResult:
    success: bool
    action: str
    path: str
    message: str


def _resolve_repo_path(relative_path: str) -> Path:
    path = (BASE / relative_path).resolve()

    if not str(path).startswith(str(BASE)):
        raise ValueError(f"Path escapes repository root: {relative_path}")

    return path


def read_file(relative_path: str) -> str:
    path = _resolve_repo_path(relative_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {relative_path}")

    return path.read_text(encoding="utf-8")


def write_file(relative_path: str, content: str) -> FileOperationResult:
    path = _resolve_repo_path(relative_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")

    return FileOperationResult(
        success=True,
        action="write_file",
        path=relative_path,
        message="File written successfully.",
    )


def append_file(relative_path: str, content: str) -> FileOperationResult:
    path = _resolve_repo_path(relative_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("a", encoding="utf-8") as f:
        f.write(content)

    return FileOperationResult(
        success=True,
        action="append_file",
        path=relative_path,
        message="Content appended successfully.",
    )


def replace_in_file(relative_path: str, old: str, new: str) -> FileOperationResult:
    path = _resolve_repo_path(relative_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {relative_path}")

    content = path.read_text(encoding="utf-8")

    match_count = content.count(old)
    if match_count == 0:
        raise ValueError(f"Target text not found in file: {relative_path}")
    if match_count > 1:
        raise ValueError(
            f"Target text matched {match_count} times in file: {relative_path}. "
            "replace_in_file requires exactly one match."
        )

    updated = content.replace(old, new, 1)
    path.write_text(updated, encoding="utf-8")

    return FileOperationResult(
        success=True,
        action="replace_in_file",
        path=relative_path,
        message="Text replaced successfully.",
    )


def file_exists(relative_path: str) -> bool:
    path = _resolve_repo_path(relative_path)
    return path.exists()


def list_files(glob_pattern: str = "**/*") -> List[str]:
    results: List[str] = []

    for path in BASE.glob(glob_pattern):
        if path.is_file():
            results.append(str(path.relative_to(BASE)))

    return sorted(results)