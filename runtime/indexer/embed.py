import json
from pathlib import Path
from openai import OpenAI

BASE = Path("/workspaces/ai-company-os/runtime/indexer")
INPUT = BASE / "doc_summaries.json"
OUTPUT = BASE / "doc_embeddings.json"

client = OpenAI()

def embed(text):
    resp = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return resp.data[0].embedding

def main():
    data = json.load(open(INPUT))
    docs = data["documents"]

    results = []

    for doc in docs:
        vector = embed(doc["summary"])
        results.append({
            "path": doc["path"],
            "purpose": doc["purpose"],
            "summary": doc["summary"],
            "embedding": vector
        })

    json.dump(results, open(OUTPUT, "w"), indent=2)

    print("Embeddings written:", OUTPUT)
    print("Docs embedded:", len(results))

if __name__ == "__main__":
    main()