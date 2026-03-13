import json
import re
from pathlib import Path
from datetime import datetime, UTC

BASE_DIR = Path("/workspaces/ai-company-os")
INDEX_FILE = BASE_DIR / "system_index.json"
OUTPUT_FILE = BASE_DIR / "runtime" / "indexer" / "doc_summaries.json"

TEXT_EXTENSIONS = {
    ".md", ".txt", ".json", ".yml", ".yaml", ".py", ".ts", ".tsx", ".js", ".jsx", ".css", ".html"
}

PURPOSE_RULES = [
    ("agents/", "agent_role_definition"),
    ("architecture/", "architecture_rule"),
    ("workflows/", "workflow_definition"),
    ("company/", "company_strategy"),
    (".github/workflows/", "automation_workflow"),
    ("schemas/", "schema_contract"),
    ("templates/", "template_artifact"),
    ("reports/", "report_artifact"),
    ("runtime/", "runtime_infrastructure"),
]

def load_index():
    with open(INDEX_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def guess_repo_root(repo_name: str) -> Path:
    if repo_name == "ai-company-os":
        return BASE_DIR
    if repo_name == "lease-lens-dash":
        return Path("/workspaces/lease-lens-dash")
    return BASE_DIR

def classify_purpose(path_str: str) -> str:
    normalized = path_str.replace("\\", "/")
    for prefix, purpose in PURPOSE_RULES:
        if normalized.startswith(prefix):
            return purpose
    return "general_project_file"

def safe_read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return ""

def extract_headings(text: str) -> list[str]:
    headings = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            headings.append(re.sub(r"^#+\s*", "", stripped))
        if len(headings) >= 8:
            break
    return headings

def first_meaningful_lines(text: str, limit: int = 8) -> list[str]:
    lines = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("#"):
            continue
        if stripped.startswith("//") or stripped.startswith("/*") or stripped.startswith("*"):
            continue
        lines.append(stripped)
        if len(lines) >= limit:
            break
    return lines

def summarize_text(name: str, path_str: str, purpose: str, text: str) -> str:
    headings = extract_headings(text)
    body_lines = first_meaningful_lines(text, limit=5)

    parts = [f"{name} is a {purpose.replace('_', ' ')} file."]
    if headings:
        parts.append(f"Main sections: {', '.join(headings[:4])}.")
    if body_lines:
        parts.append(f"Opening content: {' '.join(body_lines[:2])[:300]}")
    else:
        parts.append(f"It is located at {path_str}.")
    return " ".join(parts).strip()

def build_summaries():
    index = load_index()
    output = {
        "generated_at": datetime.now(UTC).isoformat(),
        "documents": []
    }

    for entry in index.get("files", []):
        ext = entry.get("extension", "").lower()
        if ext not in TEXT_EXTENSIONS:
            continue

        repo_root = guess_repo_root(entry["repo"])
        file_path = repo_root / entry["path"]

        if not file_path.exists():
            continue

        text = safe_read(file_path)
        purpose = classify_purpose(entry["path"])
        headings = extract_headings(text)
        intro_lines = first_meaningful_lines(text, limit=5)

        output["documents"].append({
            "repo": entry["repo"],
            "path": entry["path"],
            "name": entry["name"],
            "purpose": purpose,
            "headings": headings,
            "intro_lines": intro_lines,
            "summary": summarize_text(entry["name"], entry["path"], purpose, text),
            "size_bytes": entry["size_bytes"],
            "modified": entry["modified"],
        })

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)

    print(f"Summaries written to {OUTPUT_FILE}")
    print(f"Documents summarized: {len(output['documents'])}")

if __name__ == "__main__":
    build_summaries()