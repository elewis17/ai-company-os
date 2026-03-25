from __future__ import annotations

import os
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional


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
class GitCommandResult:
    success: bool
    command: List[str]
    stdout: str
    stderr: str
    returncode: int


def _run_git_command(args: List[str], check: bool = True) -> GitCommandResult:
    base = _get_repo_root()
    result = subprocess.run(
        ["git", *args],
        cwd=base,
        text=True,
        capture_output=True,
    )

    cmd_result = GitCommandResult(
        success=result.returncode == 0,
        command=["git", *args],
        stdout=result.stdout.strip(),
        stderr=result.stderr.strip(),
        returncode=result.returncode,
    )

    if check and result.returncode != 0:
        raise RuntimeError(
            f"Git command failed: {' '.join(cmd_result.command)}\n"
            f"stdout:\n{cmd_result.stdout}\n\nstderr:\n{cmd_result.stderr}"
        )

    return cmd_result


def get_current_branch() -> str:
    result = _run_git_command(["rev-parse", "--abbrev-ref", "HEAD"])
    return result.stdout


def create_branch(branch_name: str, checkout: bool = True) -> GitCommandResult:
    if checkout:
        return _run_git_command(["checkout", "-b", branch_name])

    return _run_git_command(["branch", branch_name])


def checkout_branch(branch_name: str) -> GitCommandResult:
    return _run_git_command(["checkout", branch_name])


def git_status() -> GitCommandResult:
    return _run_git_command(["status", "--short"], check=False)


def has_uncommitted_changes() -> bool:
    result = git_status()
    return bool(result.stdout.strip())


def git_add(paths: Optional[List[str]] = None) -> GitCommandResult:
    if paths is None or len(paths) == 0:
        return _run_git_command(["add", "."])

    return _run_git_command(["add", *paths])


def git_commit(message: str) -> GitCommandResult:
    return _run_git_command(["commit", "-m", message])


def git_push(branch_name: str, set_upstream: bool = True) -> GitCommandResult:
    if set_upstream:
        return _run_git_command(["push", "-u", "origin", branch_name])

    return _run_git_command(["push", "origin", branch_name])


def changed_files_against_head() -> List[str]:
    result = _run_git_command(["diff", "--name-only", "HEAD"], check=False)

    if not result.stdout:
        return []

    return [line.strip() for line in result.stdout.splitlines() if line.strip()]
