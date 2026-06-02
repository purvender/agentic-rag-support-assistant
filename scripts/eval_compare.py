import argparse
import json
import sys
from pathlib import Path

import chromadb
import ollama
try:
    from scripts.mlx_utils import PROJECT_ROOT, run_mlx
except ModuleNotFoundError:
    from mlx_utils import PROJECT_ROOT, run_mlx

CHROMA_DIR = PROJECT_ROOT / "chroma"
COLLECTION_NAME = "support_faqs"
EMBED_MODEL = "nomic-embed-text"
PROMPTS_PATH = PROJECT_ROOT / "data" / "eval" / "test_prompts.txt"

MODES = [
    "base_only",
    "tuned_only",
    "base_rag",
    "tuned_rag",
]


def load_questions() -> list[str]:
    if not PROMPTS_PATH.exists():
        raise FileNotFoundError(f"Missing prompts file: {PROMPTS_PATH}")
    return [
        line.strip()
        for line in PROMPTS_PATH.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def get_collection():
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    collection = client.get_or_create_collection(name=COLLECTION_NAME)
    if collection.count() == 0:
        raise RuntimeError(
            "FAQ index is empty. Run from the project root: python scripts/rag_index.py"
        )
    return collection


def retrieve_context(question: str, n_results: int = 1):
    collection = get_collection()

    query_embedding = ollama.embeddings(model=EMBED_MODEL, prompt=question)["embedding"]

    results = collection.query(query_embeddings=[query_embedding], n_results=n_results)

    docs = results["documents"][0]
    metas = results["metadatas"][0]
    context = "\n\n".join(docs)

    return context, metas


def prompt_without_rag(question: str) -> str:
    return f"""You are a customer support assistant. Answer clearly and concisely.

Customer Question:
{question}

Answer:
"""


def prompt_with_rag(question: str, context: str) -> str:
    return f"""You are a customer support assistant.
Answer the customer question using only the FAQ context below.
If the answer is not in the FAQ context, say you do not know.
Be concise and helpful.

FAQ Context:
{context}

Customer Question:
{question}

Answer:
"""


def _generate(prompt: str, use_adapter: bool) -> str:
    try:
        return run_mlx(prompt, use_adapter=use_adapter)
    except RuntimeError as exc:
        return f"[ERROR]\n{exc}"


def run_mode(question: str, mode: str):
    if mode == "base_only":
        answer = _generate(prompt_without_rag(question), use_adapter=False)
        return {"mode": mode, "sources": [], "answer": answer}

    if mode == "tuned_only":
        answer = _generate(prompt_without_rag(question), use_adapter=True)
        return {"mode": mode, "sources": [], "answer": answer}

    if mode == "base_rag":
        context, metas = retrieve_context(question, n_results=1)
        answer = _generate(prompt_with_rag(question, context), use_adapter=False)
        return {"mode": mode, "sources": metas, "answer": answer}

    if mode == "tuned_rag":
        context, metas = retrieve_context(question, n_results=1)
        answer = _generate(prompt_with_rag(question, context), use_adapter=True)
        return {"mode": mode, "sources": metas, "answer": answer}

    return {"mode": mode, "sources": [], "answer": "[ERROR] Unknown mode"}


def format_report(rows: list) -> str:
    lines = [
        "# Four-mode evaluation\n",
        "Questions from `data/eval/test_prompts.txt` across base only, tuned only, base + RAG, tuned + RAG.\n",
    ]
    for idx, item in enumerate(rows, 1):
        lines.append(f"## Q{idx}\n")
        lines.append(f"**Question:** {item['question']}\n")
        for run in item["runs"]:
            lines.append(f"### {run['mode']}\n")
            if run["sources"]:
                lines.append(
                    f"**Retrieved sources:** "
                    f"{json.dumps(run['sources'], ensure_ascii=False)}\n"
                )
            else:
                lines.append("**Retrieved sources:** None\n")
            lines.append("**Answer:**\n")
            lines.append(f"{run['answer']}\n")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Compare four MLX + RAG modes.")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Optional path to write a markdown report (default: print to stdout)",
    )
    parser.add_argument(
        "--check-retrieval",
        action="store_true",
        help="Only verify retrieval vs data/eval/expected_sources.jsonl (no MLX)",
    )
    args = parser.parse_args()

    if args.check_retrieval:
        from check_retrieval import main as check_main

        sys.exit(check_main())

    questions = load_questions()
    rows = []

    for i, question in enumerate(questions, 1):
        print(f"[{i}/{len(questions)}] {question}", file=sys.stderr)
        item = {"question": question, "runs": []}
        for mode in MODES:
            print(f"  -> {mode}", file=sys.stderr)
            item["runs"].append(run_mode(question, mode))
        rows.append(item)

    report = format_report(rows)

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(report, encoding="utf-8")
        print(f"Wrote comparison report to {args.output}", file=sys.stderr)
    else:
        print(report)


if __name__ == "__main__":
    main()
