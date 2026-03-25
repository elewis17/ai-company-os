from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import List


_DEFAULT_BASE = Path(__file__).resolve().parents[2]
_BASE_ENV_VAR = "LEASE_LENS_REPO_ROOT"


def _get_repo_root() -> Path:
    configured_root = os.environ.get(_BASE_ENV_VAR)
    if configured_root:
        base = Path(configured_root).expanduser().resolve()
    else:
        base = _DEFAULT_BASE.resolve()
    return base


@dataclass
class FileOperationResult:
    success: bool
    action: str
    path: str
    message: str


def _resolve_repo_path(relative_path: str) -> Path:
    base = _get_repo_root()
    path = (base / relative_path).resolve()

    if not str(path).startswith(str(base)):
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

    if old not in content:
        raise ValueError(f"Target text not found in file: {relative_path}")

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
    base = _get_repo_root()
    results: List[str] = []

    for path in base.glob(glob_pattern):
        if path.is_file():
            results.append(str(path.relative_to(base)))

    return sorted(results)
