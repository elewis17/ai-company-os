from __future__ import annotations

from typing import Any, Dict, List

from runtime.tools.repo_tools import (
    append_file,
    file_exists,
    read_file,
    replace_in_file,
    write_file,
)


def apply_file_operations(file_operations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    results: List[Dict[str, Any]] = []

    for op in file_operations:
        action = op.get("action")
        path = op.get("path")

        if not action:
            raise ValueError("File operation is missing 'action'")

        if not path:
            raise ValueError("File operation is missing 'path'")

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