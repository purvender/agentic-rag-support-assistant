"""Verify RAG retrieval hits expected FAQ files (no MLX generation)."""
import json
import sys
from pathlib import Path

import chromadb
import ollama
try:
    from scripts.mlx_utils import PROJECT_ROOT
except ModuleNotFoundError:
    from mlx_utils import PROJECT_ROOT

CHROMA_DIR = PROJECT_ROOT / "chroma"
COLLECTION_NAME = "support_faqs"
EMBED_MODEL = "nomic-embed-text"
EXPECTED_PATH = PROJECT_ROOT / "data" / "eval" / "expected_sources.jsonl"


def load_expected() -> list[dict]:
    rows = []
    for line in EXPECTED_PATH.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            rows.append(json.loads(line))
    return rows


def main() -> int:
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    collection = client.get_or_create_collection(name=COLLECTION_NAME)
    if collection.count() == 0:
        print("Error: FAQ index is empty. Run: python scripts/rag_index.py", file=sys.stderr)
        return 1

    cases = load_expected()
    passed = 0
    failed = 0

    for case in cases:
        question = case["question"]
        expected = case["expected_source"]
        embedding = ollama.embeddings(model=EMBED_MODEL, prompt=question)["embedding"]
        results = collection.query(query_embeddings=[embedding], n_results=1)
        got = results["metadatas"][0][0]["source"]
        ok = got == expected
        status = "PASS" if ok else "FAIL"
        print(f"{status}  expected={expected}  got={got}")
        print(f"       Q: {question[:70]}...")
        if ok:
            passed += 1
        else:
            failed += 1

    print(f"\nRetrieval check: {passed}/{len(cases)} passed, {failed} failed.")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
