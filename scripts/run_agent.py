import json
import subprocess
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
RETRIEVER = BASE / "runtime/indexer/retrieve.py"
RETRIEVED = BASE / "runtime/indexer/retrieved_paths.json"

title = sys.argv[1]
body = sys.argv[2] if len(sys.argv) > 2 else ""

query = f"{title}\n{body}"

print("Running retriever...")

subprocess.run(
    ["python", str(RETRIEVER), query],
    check=True
)

print("Loading retrieved files...")

paths = json.load(open(RETRIEVED))

print("\nRelevant files:\n")

for p in paths:
    print("-", p["path"])