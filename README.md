# Apple Silicon LoRA RAG Support Assistant

A local, beginner-friendly customer support assistant for macOS Apple Silicon using:

- **MLX LoRA fine-tuning**
- **Ollama embeddings**
- **ChromaDB**
- **RAG (Retrieval-Augmented Generation)**

This project shows how to build a support bot that can answer questions from local FAQ files and speak in a support-friendly tone.

---

## What this project is

This repository is a learning project and implementation guide for a **local support assistant**.

It runs fully on-device on **Apple Silicon Mac** and demonstrates two important ideas:

1. **Fine-tuning** for response style and tone.
2. **RAG** for factual grounding from local documents.

In simple words:

- the model learns **how to talk** using LoRA fine-tuning,
- the system learns **what to answer** using FAQ retrieval.

---

## Why this project exists

A plain LLM can sound fluent, but it may guess or hallucinate.

A plain RAG system is better because it retrieves real documents before answering.

This repository is designed so a beginner can understand that journey step by step.

---

## What is RAG?

**RAG** means **Retrieval-Augmented Generation**.[web:1314]

Simple meaning:

1. Read user question.
2. Search the knowledge base.
3. Pick the most relevant text.
4. Put that text into the prompt.
5. Let the model answer using that context.

That helps the model answer using **real project documents** instead of only guessing from training.

---

## Features

### Current core features

- Local support assistant for **macOS Apple Silicon**
- **MLX LoRA fine-tuning** with Llama 3.2 1B
- **Ollama** embeddings using `nomic-embed-text`
- **ChromaDB** vector storage
- Local FAQ retrieval from `docs/faqs/`
- Four-mode comparison:
  - base only
  - tuned only
  - base + RAG
  - tuned + RAG

---

## Who this repo is for

This repo is useful for:

- beginners learning **RAG**
- developers learning **local AI on Apple Silicon**
- engineers learning the difference between:
  - fine-tuning
  - embeddings
  - vector search
  - retrieval
- anyone who wants a small, readable AI engineering project

---

## Tech stack

| Layer | Tool |
|------|------|
| Base model | `mlx-community/Llama-3.2-1B-Instruct-4bit` |
| Fine-tuning | `mlx-lm` LoRA |
| Embeddings | Ollama `nomic-embed-text` |
| Vector database | ChromaDB |
| Language | Python |
| Platform | macOS Apple Silicon |

---

## Project idea in one sentence

This project builds a fictional support assistant that answers from local FAQ documents and speaks in a support tone.

---

## What is included in the repo

Everything below is included so a new user can clone and run the project quickly:

| Included | Location | Purpose |
|----------|----------|---------|
| Pre-trained LoRA adapters | `adapters-llama3-1b/` | Run the tuned model immediately |
| Training data | `data/support/*.jsonl` | Re-train or study the fine-tuning format |
| FAQ documents | `docs/faqs/*.txt` | Knowledge base for retrieval |
| Eval prompts | `data/eval/test_prompts.txt` | Four-mode evaluation |
| Scripts | `scripts/` | Index, query, evaluate |

### Not stored in GitHub

These are created locally on your machine:

| Artifact | Why |
|----------|-----|
| `chroma/` | Local vector index generated from FAQs |
| `.venv/` | Your local Python environment |
| `compare_results.md` | Optional local evaluation output |
| Base model weights | Downloaded locally by MLX |

---

## Prerequisites

You need:

- **macOS**
- **Apple Silicon**
- **Python 3.9+**
- **Ollama** installed and running locally

Install the embedding model:

```bash
ollama pull nomic-embed-text
```

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install Python dependencies:

```bash
pip install -r requirements.txt
```

Pre-cache the base MLX model once so later runs are smoother:

```bash
python -m mlx_lm generate \
  --model mlx-community/Llama-3.2-1B-Instruct-4bit \
  --prompt "hi" \
  --max-tokens 1
```

Keep **Ollama running** before indexing or querying.

---

## Quick start

This is the fastest path.

### 1. Clone the repo

```bash
git clone https://github.com/purvender/apple-silicon-lora-rag-support-assistant.git
cd apple-silicon-lora-rag-support-assistant
```

### 2. Set up environment

```bash
ollama pull nomic-embed-text

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

### 3. Build the vector index once

```bash
python scripts/rag_index.py
```

### 4. Ask a question with plain RAG

```bash
python scripts/rag_query.py "Can I get a refund for my annual plan?"
```

### 5. Run quick checks

```bash
bash scripts/smoke_test.sh
```

---

## Two ways to use this project

## Path A — Use the pre-trained model

This is the easiest path.

You do **not** need to fine-tune anything.

Run:

```bash
python scripts/rag_index.py
python scripts/rag_query.py "Can I get a refund for my annual plan?"
```

Use this path if you want to:
- learn the flow,
- try the project quickly,
- inspect the outputs,
- understand the architecture first.

---

## Path B — Train your own LoRA adapters

Use this path if you want to learn or customize the assistant.

### 1. Edit training data

Modify:

- `data/support/train.jsonl`
- `data/support/valid.jsonl`
- `data/support/test.jsonl`

Each line should be one JSON object with:
- `prompt`
- `completion`

### 2. Fine-tune

```bash
source .venv/bin/activate

mlx_lm.lora \
  --model mlx-community/Llama-3.2-1B-Instruct-4bit \
  --train \
  --data ./data/support \
  --adapter-path ./adapters-llama3-1b \
  --iters 100 \
  --batch-size 4 \
  --learning-rate 1e-5 \
  --num-layers 16
```

### 3. Rebuild the index and query

```bash
python scripts/rag_index.py
python scripts/rag_query.py "Your question here"
```

---

## How the plain RAG system works

This is the original pipeline:

```text
User question
   -> embed with Ollama
   -> search ChromaDB
   -> retrieve top FAQ text
   -> build prompt with retrieved context
   -> generate answer with MLX + LoRA
   -> return answer
```

This is the **plain RAG support assistant**.

---

## Why we use both fine-tuning and RAG

These two things solve different problems.

| Technique | What it improves |
|----------|------------------|
| Fine-tuning | Tone, structure, support style |
| RAG | Factual grounding from editable documents |

Simple rule:

- **Fine-tuning** teaches the model **how to answer**
- **RAG** provides the content for **what to answer**

---

## Project structure

```text
apple-silicon-lora-rag-support-assistant/
├── README.md
├── LICENSE
├── CONTRIBUTING.md
├── requirements.txt
├── .gitignore
├── data/
│   ├── support/
│   │   ├── train.jsonl
│   │   ├── valid.jsonl
│   │   └── test.jsonl
│   └── eval/
│       ├── test_prompts.txt
│       └── expected_sources.jsonl
├── docs/
│   ├── LEARNING.md
│   ├── TROUBLESHOOTING.md
│   ├── example_compare_results.md
│   └── faqs/
│       ├── refunds.txt
│       ├── billing.txt
│       ├── passwords.txt
│       ├── trial_extensions.txt
│       ├── account_setup.txt
│       ├── cancellation.txt
│       ├── team_permissions.txt
│       └── support.txt
├── scripts/
│   ├── mlx_utils.py
│   ├── rag_index.py
│   ├── rag_query.py
│   ├── eval_compare.py
│   ├── check_retrieval.py
│   └── smoke_test.sh
├── adapters-llama3-1b/
└── chroma/
```

---

## File guide for beginners

### `scripts/rag_index.py`
Builds the ChromaDB vector index from the FAQ text files.

### `scripts/rag_query.py`
Runs the plain RAG assistant.

### `scripts/eval_compare.py`
Compares base vs tuned vs RAG combinations.

### `scripts/check_retrieval.py`
Checks retrieval quality quickly without full generation.

### `scripts/smoke_test.sh`
Runs a quick local validation.

---

## FAQ documents

The knowledge base lives in `docs/faqs/`.

| File | Topic |
|------|------|
| `refunds.txt` | Annual refund window |
| `billing.txt` | Invoices, billing email, plan changes |
| `passwords.txt` | Password reset |
| `trial_extensions.txt` | Trial extension, teammate limit |
| `account_setup.txt` | Sign-up and verification |
| `cancellation.txt` | Cancel, read-only period, data deletion |
| `team_permissions.txt` | Invites, roles, permissions |
| `support.txt` | How to contact support |

If you edit any of these files, rebuild the index:

```bash
python scripts/rag_index.py
```

---

## Plain RAG usage

Ask a support question:

```bash
python scripts/rag_query.py "Can I cancel my plan and still access my data?"
```

Use this mode if you want:
- the simplest system,
- direct RAG behavior,
- easy debugging.

---

## Evaluation

## Four-mode comparison

This compares:
- base only
- tuned only
- base + RAG
- tuned + RAG

Run:

```bash
python scripts/eval_compare.py -o compare_results.md
```

For a sample output, see:

- `docs/example_compare_results.md`

## Retrieval-only check

This checks retrieval quality quickly without full generation:

```bash
python scripts/check_retrieval.py
```

---

## Beginner learning path

If you are new, use this order:

### Step 1
Read this README fully.

### Step 2
Run:

```bash
python scripts/rag_index.py
```

### Step 3
Run plain RAG:

```bash
python scripts/rag_query.py "Can I get a refund for my annual plan?"
```

### Step 4
Read these files in this order:

1. `scripts/rag_index.py`
2. `scripts/rag_query.py`
3. `scripts/check_retrieval.py`
4. `scripts/eval_compare.py`

That order makes the architecture easier to understand.

---

## What changed from the original repo

Originally, this project was mainly a **local LoRA + RAG support assistant**.

Now it is being prepared for a future **agentic RAG** upgrade.

### Current version
- retrieve FAQ
- answer using retrieved context

### Planned next version
- understand request type
- choose next action
- retrieve / summarize / escalate / clarify
- then answer

This future agentic layer is **not yet implemented** in the current repo.

---

## Planned future improvements

Possible next steps:

- persistent conversation memory
- better retrieval ranking
- real issue history search
- real ticket system integration
- web UI or API layer
- agentic workflow with routing and tools
- richer evaluation metrics
- multi-turn troubleshooting flows

---

## Troubleshooting

If something fails:

- make sure **Ollama is running**
- make sure `nomic-embed-text` is pulled
- make sure the virtual environment is active
- make sure the vector index exists

Useful docs:
- `docs/TROUBLESHOOTING.md`
- `docs/LEARNING.md`

---

## Support this project

This repository is free to use for learning and experimentation.

If it helps you:
- star the repository
- share it
- fork it and improve it
- use it as a base for your own local support assistant

---

## Disclaimer

This is educational lab software only.

It is **not** production customer support software, and it is **not** legal or billing advice.

All AcornDesk content in this repository is fictional.

---

## License

- **This repository:** MIT — see `LICENSE`
- Review the licenses of all external dependencies before redistribution:
  - MLX
  - mlx-lm
  - Ollama models
  - base model weights