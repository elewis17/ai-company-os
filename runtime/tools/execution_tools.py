from __future__ import annotations

import ast
import json
import re
from pathlib import Path
from typing import Any, Dict, List, Tuple

from runtime.tools.repo_tools import (
    append_file,
    file_exists,
    read_file,
    replace_in_file,
    write_file,
)


WRITE_ACTIONS = {"write_file", "append_file", "replace_in_file"}

SUSPICIOUS_TRAILING_PATTERNS = (
    r"```[\s\r\n]*[\]\}\),]+[\s\r\n,]*$",
    r"[\]\}]{1,2},\s*$",
    r"[\]\}]{1,2},\s*['\"]\s*$",
)


def _validate_file_operations(file_operations: List[Dict[str, Any]]) -> None:
    path_actions: Dict[str, List[Tuple[int, str]]] = {}

    for idx, op in enumerate(file_operations):
        action = op.get("action")
        path = op.get("path")

        if not action:
            raise ValueError("File operation is missing 'action'")

        if not path:
            raise ValueError("File operation is missing 'path'")

        if action in WRITE_ACTIONS:
            path_actions.setdefault(path, []).append((idx, action))

    for path, ops in path_actions.items():
        actions = [action for _, action in ops]
        unique_actions = set(actions)

        if len(ops) > 1:
            raise ValueError(
                f"Conflicting file operations for '{path}' in a single step: {actions}. "
                "Only one write operation per file is allowed per step."
            )

        if "replace_in_file" in unique_actions and "append_file" in unique_actions:
            raise ValueError(
                f"Invalid operation batch for '{path}': cannot combine replace_in_file "
                "and append_file in the same step."
            )

        if "write_file" in unique_actions and "append_file" in unique_actions:
            raise ValueError(
                f"Invalid operation batch for '{path}': cannot combine write_file "
                "and append_file in the same step."
            )

        if "write_file" in unique_actions and "replace_in_file" in unique_actions:
            raise ValueError(
                f"Invalid operation batch for '{path}': cannot combine write_file "
                "and replace_in_file in the same step."
            )


def _normalize_text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).replace("\r\n", "\n").strip()


def _count_lines(text: str) -> int:
    if not text:
        return 0
    return text.count("\n") + 1


def _changed_line_count(before: str, after: str) -> int:
    before_lines = before.splitlines()
    after_lines = after.splitlines()
    max_len = max(len(before_lines), len(after_lines))
    changed = 0

    for idx in range(max_len):
        old_line = before_lines[idx] if idx < len(before_lines) else None
        new_line = after_lines[idx] if idx < len(after_lines) else None
        if old_line != new_line:
            changed += 1

    return changed


def _reject_suspicious_trailing_artifacts(path: str, content: str) -> None:
    stripped = content.rstrip()

    for pattern in SUSPICIOUS_TRAILING_PATTERNS:
        if re.search(pattern, stripped):
            raise ValueError(
                f"Generated content for '{path}' appears malformed or has trailing artifact residue."
            )

    suspicious_phrases = (
        "Return only schema-compliant JSON",
        "You are executing the role",
        '"file_operations"',
        '"action"',
        '"path"',
    )

    for phrase in suspicious_phrases:
        if phrase in content:
            raise ValueError(
                f"Generated content for '{path}' appears to contain prompt/schema leakage."
            )


def _validate_markdown_content(path: str, content: str) -> None:
    _reject_suspicious_trailing_artifacts(path, content)

    fence_count = content.count("```")
    if fence_count % 2 != 0:
        raise ValueError(f"Markdown validation failed for '{path}': unbalanced code fences.")


def _validate_json_content(path: str, content: str) -> None:
    _reject_suspicious_trailing_artifacts(path, content)

    try:
        json.loads(content)
    except json.JSONDecodeError as exc:
        raise ValueError(f"JSON validation failed for '{path}': {exc}") from exc


def _validate_python_content(path: str, content: str) -> None:
    _reject_suspicious_trailing_artifacts(path, content)

    try:
        ast.parse(content)
    except SyntaxError as exc:
        raise ValueError(f"Python validation failed for '{path}': {exc}") from exc


def _validate_text_content(path: str, content: str) -> None:
    _reject_suspicious_trailing_artifacts(path, content)


def _validate_candidate_file(path: str, content: str) -> None:
    suffix = Path(path).suffix.lower()

    if suffix == ".json":
        _validate_json_content(path, content)
    elif suffix == ".py":
        _validate_python_content(path, content)
    elif suffix in {".md", ".markdown"}:
        _validate_markdown_content(path, content)
    else:
        _validate_text_content(path, content)


def _validate_diff_budget(path: str, before: str, after: str, action: str) -> None:
    if action == "write_file":
        return

    changed_lines = _changed_line_count(before, after)
    before_line_count = _count_lines(before)
    after_line_count = _count_lines(after)
    max_line_count = max(before_line_count, after_line_count)

    if max_line_count == 0:
        return

    if changed_lines > 200:
        raise ValueError(
            f"Change to '{path}' is too large for a single {action} operation "
            f"({changed_lines} changed lines)."
        )

    if before_line_count > 0 and changed_lines > max(50, int(before_line_count * 0.8)):
        raise ValueError(
            f"Change to '{path}' appears too broad for {action} "
            f"({changed_lines}/{before_line_count} lines changed)."
        )


def _validate_operation_payload(op: Dict[str, Any]) -> None:
    action = op.get("action")
    path = op.get("path")

    if action == "write_file":
        content = op.get("content")
        if content is None:
            raise ValueError(f"write_file requires 'content' for '{path}'")

        candidate = str(content)
        _validate_candidate_file(path, candidate)

    elif action == "append_file":
        content = op.get("content")
        if content is None:
            raise ValueError(f"append_file requires 'content' for '{path}'")

        existing_content = read_file(path) if file_exists(path) else ""
        normalized_existing = _normalize_text(existing_content)
        normalized_append = _normalize_text(content)

        if normalized_append and normalized_append in normalized_existing:
            raise ValueError(
                f"append_file for '{path}' appears to duplicate content already present in the file."
            )

        candidate = existing_content + str(content)
        _validate_candidate_file(path, candidate)
        _validate_diff_budget(path, existing_content, candidate, action)

    elif action == "replace_in_file":
        old = op.get("old")
        new = op.get("new")

        if old is None or new is None:
            raise ValueError(
                "replace_in_file requires 'old' and 'new' fields"
            )

        existing_content = read_file(path) if file_exists(path) else None
        if existing_content is None:
            raise ValueError(
                f"replace_in_file cannot run because '{path}' does not exist."
            )

        old_text = str(old)
        new_text = str(new)

        match_count = existing_content.count(old_text)
        if match_count == 0:
            raise ValueError(
                f"replace_in_file could not find the target text in '{path}'."
            )
        if match_count > 1:
            raise ValueError(
                f"replace_in_file matched the target text {match_count} times in '{path}'. "
                "Expected exactly one match."
            )

        candidate = existing_content.replace(old_text, new_text, 1)
        _validate_candidate_file(path, candidate)
        _validate_diff_budget(path, existing_content, candidate, action)


def apply_file_operations(file_operations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    results: List[Dict[str, Any]] = []

    _validate_file_operations(file_operations)

    for op in file_operations:
        action = op.get("action")
        path = op.get("path")

        if not action:
            raise ValueError("File operation is missing 'action'")

        if not path:
            raise ValueError("File operation is missing 'path'")

        if action in WRITE_ACTIONS:
            _validate_operation_payload(op)

        if action == "write_file":
            content = op.get("content", "")
            result = write_file(path, content)

        elif action == "append_file":
            content = op.get("content", "")
            result = append_file(path, content)

        elif action == "replace_in_file":
            old = op.get("old")
            new = op.get("new")

            if old is None or new is None:
                raise ValueError(
                    "replace_in_file requires 'old' and 'new' fields"
                )

            result = replace_in_file(path, old, new)

        elif action == "read_file":
            content = read_file(path)
            results.append(
                {
                    "success": True,
                    "action": action,
                    "path": path,
                    "message": "File read successfully.",
                    "content": content,
                }
            )
            continue

        elif action == "file_exists":
            exists = file_exists(path)
            results.append(
                {
                    "success": True,
                    "action": action,
                    "path": path,
                    "message": "File existence checked successfully.",
                    "exists": exists,
                }
            )
            continue

        else:
            raise ValueError(f"Unsupported file operation: {action}")

        results.append(
            {
                "success": result.success,
                "action": result.action,
                "path": result.path,
                "message": result.message,
            }
        )

    return results