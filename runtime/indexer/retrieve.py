import json
import math
import sys
from pathlib import Path
from openai import OpenAI

BASE = Path(__file__).resolve().parent
EMBED_FILE = BASE / "doc_embeddings.json"
OUT_FILE = BASE / "retrieved_paths.json"

client = OpenAI()


def cosine_similarity(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def embed_query(text: str):
    resp = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return resp.data[0].embedding


def retrieve(query: str, top_k: int = 5):
    if not EMBED_FILE.exists():
        raise FileNotFoundError(f"Embeddings file not found: {EMBED_FILE}")

    with open(EMBED_FILE, "r", encoding="utf-8") as f:
        docs = json.load(f)

    q_vec = embed_query(query)
    scored = []

    for doc in docs:
        embedding = doc.get("embedding")
        if not embedding:
            continue

        score = cosine_similarity(q_vec, embedding)
        scored.append({
            "score": score,
            "path": doc.get("path", ""),
            "purpose": doc.get("purpose", ""),
            "summary": doc.get("summary", "")
        })

    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:top_k]


if __name__ == "__main__":
    query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "default issue query"
    results = retrieve(query, top_k=5)

    with open(OUT_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print(f"Wrote {len(results)} results to {OUT_FILE}")
    for r in results:
        print(f"{r['score']:.4f} | {r['path']}")