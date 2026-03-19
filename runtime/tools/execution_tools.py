from __future__ import annotations

from typing import Any, Dict, List, Tuple

from runtime.tools.repo_tools import (
    append_file,
    file_exists,
    read_file,
    replace_in_file,
    write_file,
)


WRITE_ACTIONS = {"write_file", "append_file", "replace_in_file"}


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


def _validate_operation_payload(op: Dict[str, Any]) -> None:
    action = op.get("action")
    path = op.get("path")

    if action == "write_file":
        content = op.get("content")
        if content is None:
            raise ValueError(f"write_file requires 'content' for '{path}'")

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

        if str(old) not in existing_content:
            raise ValueError(
                f"replace_in_file could not find the target text in '{path}'."
            )


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