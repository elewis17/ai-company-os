import os
import json
from pathlib import Path
from datetime import datetime

# CONFIG
PRODUCT_REPO = "../lease-lens-dash"
OS_REPO = "../ai-company-os"
OUTPUT_FILE = "system_index.json"

EXCLUDE_DIRS = {
    ".git",
    "node_modules",
    ".next",
    "dist",
    "build",
    "__pycache__"
}

def scan_repo(repo_path, repo_name):
    index = []
    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]

        for file in files:
            path = Path(root) / file
            stat = path.stat()

            index.append({
                "repo": repo_name,
                "path": str(path.relative_to(repo_path)),
                "name": file,
                "extension": path.suffix,
                "size_bytes": stat.st_size,
                "modified": datetime.fromtimestamp(stat.st_mtime).isoformat()
            })

    return index


def build_index():
    system_index = {
        "generated_at": datetime.utcnow().isoformat(),
        "files": []
    }

    system_index["files"].extend(
        scan_repo(PRODUCT_REPO, "lease-lens-dash")
    )

    system_index["files"].extend(
        scan_repo(OS_REPO, "ai-company-os")
    )

    with open(OUTPUT_FILE, "w") as f:
        json.dump(system_index, f, indent=2)

    print(f"Index written to {OUTPUT_FILE}")
    print(f"Files indexed: {len(system_index['files'])}")


if __name__ == "__main__":
    build_index()
