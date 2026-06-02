import sys

import chromadb
import ollama
try:
    from scripts.mlx_utils import PROJECT_ROOT, run_mlx
except ModuleNotFoundError:
    from mlx_utils import PROJECT_ROOT, run_mlx

CHROMA_DIR = PROJECT_ROOT / "chroma"
COLLECTION_NAME = "support_faqs"
EMBED_MODEL = "nomic-embed-text"


def _get_collection():
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    collection = client.get_or_create_collection(name=COLLECTION_NAME)
    if collection.count() == 0:
        raise RuntimeError(
            "FAQ index is empty. Run from the project root:\n  python scripts/rag_index.py"
        )
    return collection


def retrieve_context_only(query: str):
    """
    Return retrieved docs as a list of dicts:
    [
      {"source": "...", "content": "...", "score": 0.12},
      ...
    ]
    """
    collection = _get_collection()
    query_embedding = ollama.embeddings(model=EMBED_MODEL, prompt=query)["embedding"]
    results = collection.query(query_embeddings=[query_embedding], n_results=1)
    docs = results["documents"][0]
    metas = results["metadatas"][0]
    distances = results.get("distances", [[]])[0]

    retrieved = []
    for i, doc in enumerate(docs):
        meta = metas[i] if i < len(metas) else {}
        score = distances[i] if i < len(distances) else None
        retrieved.append(
            {
                "source": meta.get("source", "unknown"),
                "content": doc,
                "score": score,
            }
        )
    return retrieved


def generate_answer(query: str, retrieved_docs, use_lora: bool = True):
    context = "\n\n".join(d["content"] for d in retrieved_docs if d.get("content"))
    prompt = f"""You are a customer support assistant.
Answer the customer question using only the FAQ context below.
If the answer is not in the FAQ context, say you do not know.
Be concise and helpful.

FAQ Context:
{context}

Customer Question:
{query}

Answer:
"""
    return run_mlx(prompt, use_adapter=use_lora)


def main():
    if len(sys.argv) < 2:
        print('Usage: python scripts/rag_query.py "your question here"')
        print("Run from the project root after indexing: python scripts/rag_index.py")
        sys.exit(1)

    question = sys.argv[1]
    try:
        retrieved_docs = retrieve_context_only(question)
        answer = generate_answer(question, retrieved_docs, use_lora=True)
    except RuntimeError as exc:
        print("Error running RAG query:")
        print(exc)
        sys.exit(1)

    print("\n--- Retrieved Sources ---")
    for doc in retrieved_docs:
        print({"source": doc.get("source", "unknown")})

    print("\n--- Answer ---\n")
    print(answer)


if __name__ == "__main__":
    main()
