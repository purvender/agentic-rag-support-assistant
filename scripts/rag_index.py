from pathlib import Path

import chromadb
import ollama

PROJECT_ROOT = Path(__file__).resolve().parent.parent
FAQ_DIR = PROJECT_ROOT / "docs" / "faqs"
CHROMA_DIR = PROJECT_ROOT / "chroma"
COLLECTION_NAME = "support_faqs"
EMBED_MODEL = "nomic-embed-text"

client = chromadb.PersistentClient(path=str(CHROMA_DIR))

try:
    client.delete_collection(name=COLLECTION_NAME)
except Exception:
    pass

collection = client.get_or_create_collection(name=COLLECTION_NAME)

docs = []
ids = []
embeddings = []
metadatas = []

for path in sorted(FAQ_DIR.glob("*.txt")):
    text = path.read_text(encoding="utf-8").strip()
    if not text:
        continue

    response = ollama.embeddings(model=EMBED_MODEL, prompt=text)

    docs.append(text)
    ids.append(path.name)
    embeddings.append(response["embedding"])
    metadatas.append({"source": path.name})

if docs:
    collection.add(
        documents=docs,
        ids=ids,
        embeddings=embeddings,
        metadatas=metadatas,
    )

print(f"Indexed {len(docs)} FAQ files into {COLLECTION_NAME}.")
