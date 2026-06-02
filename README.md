# apple-silicon-lora-rag-support-assistant

A local customer support assistant for macOS Apple Silicon using **MLX LoRA fine-tuning**, **Ollama embeddings**, **ChromaDB**, and **RAG**. Fine-tuning shapes support tone and structure; retrieval grounds answers in editable FAQ documents.

**Learn:** [docs/LEARNING.md](docs/LEARNING.md) · **Fix issues:** [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) · **Contribute:** [CONTRIBUTING.md](CONTRIBUTING.md)

## Overview

This repo demonstrates a fictional **AcornDesk** support bot that can:

- answer in a support-oriented style (LoRA on Llama 3.2 1B),
- retrieve policy text from local FAQs (Chroma + `nomic-embed-text`),
- run fully on-device,
- compare **four modes**: base / tuned × with / without RAG.

**Workflow:** prepare JSONL data → fine-tune LoRA → index FAQs → query → evaluate.

## Prerequisites

- **macOS** with **Apple Silicon**
- **Python 3.9+** (tested with 3.9.6)
- **[Ollama](https://ollama.com)** running locally

```bash
ollama pull nomic-embed-text

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

The base MLX model (`mlx-community/Llama-3.2-1B-Instruct-4bit`) downloads on first generation. Pre-cache it to avoid network errors during long eval runs:

```bash
python -m mlx_lm generate \
  --model mlx-community/Llama-3.2-1B-Instruct-4bit \
  --prompt "hi" \
  --max-tokens 1
```

Keep the **Ollama app running** (or `ollama serve`) before indexing or querying.

## What is included on GitHub

Everything below is **in the repo** so a new user can clone and run without creating data from scratch:

| Included | Location | Purpose |
|----------|----------|---------|
| **Pre-trained LoRA adapters** | `adapters-llama3-1b/adapters.safetensors` | Use the AcornDesk-tuned model immediately |
| **Training data** | `data/support/*.jsonl` | Re-train or fine-tune on your own machine |
| **FAQ documents** | `docs/faqs/*.txt` (8 files) | RAG knowledge base (fictional AcornDesk policies) |
| **Eval questions** | `data/eval/test_prompts.txt` | Optional four-mode comparison |
| **Scripts** | `scripts/` | Index, query, evaluate |

**Not in the repo (created locally):**

| Artifact | Why |
|----------|-----|
| `chroma/` | Vector index built on your machine from the FAQs |
| `.venv/` | Your Python environment |
| `compare_results.md` | Optional eval output (gitignored) |
| Base Llama weights | Downloaded once by MLX from Hugging Face |

## New user: two paths

### Path A — Use the trained model (recommended)

Use the adapters and FAQs already in the repo. You do **not** need to train.

```bash
git clone https://github.com/purvenderhooda/apple-silicon-lora-rag-support-assistant.git
cd apple-silicon-lora-rag-support-assistant

ollama pull nomic-embed-text

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

# Build the FAQ search index once (or after you edit docs/faqs/)
python scripts/rag_index.py

# Ask questions (tuned model + RAG)
python scripts/rag_query.py "Can I get a refund for my annual plan?"
```

Optional quick check: `bash scripts/smoke_test.sh`

You only re-run `rag_index.py` when:

- it is your first time on this machine,
- you changed or added files under `docs/faqs/`,
- or you deleted the `chroma/` folder.

### Path B — Train your own LoRA adapters

Use the sample JSONL to learn the format, or replace it with your own support conversations.

1. Edit or replace `data/support/train.jsonl`, `valid.jsonl`, and `test.jsonl` (one JSON object per line: `prompt` + `completion`).
2. Fine-tune (overwrites or creates adapters under `adapters-llama3-1b/`):

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

3. Index FAQs and query (same as Path A):

```bash
python scripts/rag_index.py
python scripts/rag_query.py "Your question here"
```

### Custom FAQs (your own policies)

1. Add or edit `.txt` files in `docs/faqs/` (short, explicit policy text works best).
2. Re-embed and rebuild the index:

```bash
python scripts/rag_index.py
```

Embeddings are computed with **Ollama** (`nomic-embed-text`), not MLX. Each FAQ file becomes one vector in ChromaDB.

## Project structure

```text
apple-silicon-lora-rag-support-assistant/
├── README.md
├── LICENSE
├── requirements.txt
├── .gitignore
├── agent/
│   ├── types.py
│   ├── memory.py
│   ├── prompts.py
│   ├── router.py
│   ├── tools.py
│   └── orchestrator.py
├── data/
│   ├── support/          # LoRA train / valid / test JSONL
│   └── eval/
│       ├── test_prompts.txt
│       ├── expected_sources.jsonl
│       └── agent_scenarios.json
├── docs/
│   ├── LEARNING.md
│   ├── TROUBLESHOOTING.md
│   ├── faqs/
│   └── example_compare_results.md
├── scripts/
│   ├── mlx_utils.py
│   ├── rag_index.py
│   ├── rag_query.py
│   ├── agent_chat.py
│   ├── eval_agent.py
│   ├── eval_compare.py
│   ├── check_retrieval.py
│   └── smoke_test.sh
├── adapters-llama3-1b/   # trained LoRA weights (included)
└── chroma/               # local vector DB (gitignored, created by rag_index)
```

**Where outputs go**

| Artifact | Location |
|----------|----------|
| Chroma index | `chroma/` (gitignored) |
| Eval report | Project root only if you pass `-o compare_results.md` or redirect stdout (gitignored) |
| `data/eval/` | **Input prompts only** — not an output folder |

## Quick start

See **Path A** above. From the project root:

```bash
source .venv/bin/activate
bash scripts/smoke_test.sh
python scripts/rag_query.py "Can I get a refund for my annual plan?"
```

## Index FAQs (embedding step)

`rag_index.py` reads every `docs/faqs/*.txt`, calls Ollama to embed each file, and stores vectors in `chroma/`. Run once per machine (or after FAQ edits):

```bash
python scripts/rag_index.py
```

Re-running deletes and rebuilds the collection (safe to run twice).

## Query (tuned + RAG)

```bash
python scripts/rag_query.py "Can I get a refund for my annual plan?"
```

If the index is empty, the script exits with instructions to run `rag_index.py` first.

## Four-mode evaluation

Uses all lines in `data/eval/test_prompts.txt`:

| Mode | LoRA | RAG |
|------|------|-----|
| `base_only` | No | No |
| `tuned_only` | Yes | No |
| `base_rag` | No | Yes |
| `tuned_rag` | Yes | Yes |

```bash
# ~8+ minutes for 10 questions × 4 modes on M1/M2-class Apple Silicon
python scripts/eval_compare.py -o compare_results.md
```

Progress on **stderr**; report on **stdout** unless `-o` is set.  
For a sample four-mode run, see `docs/example_compare_results.md`.

Fast retrieval-only check (no MLX, ~seconds):

```bash
python scripts/check_retrieval.py
# or
python scripts/eval_compare.py --check-retrieval
```

## Agentic RAG (v1)

This project now includes a minimal agent orchestration layer on top of the original RAG pipeline.

### What the agent adds

- intent classification
- tool-based workflow
- lightweight conversation memory
- clarification when retrieval is weak
- escalation path for high-risk or human-handoff requests

### New files

- `agent/router.py` — intent routing
- `agent/tools.py` — retrieval, summarization, escalation, response drafting
- `agent/memory.py` — issue summary and attempted steps
- `agent/orchestrator.py` — main workflow
- `scripts/agent_chat.py` — CLI entrypoint for the agent
- `scripts/eval_agent.py` — simple evaluation harness

### Run the agent

```bash
python scripts/agent_chat.py "I didn't receive the password reset email"
```

### Evaluate the agent

```bash
python scripts/eval_agent.py
```

## Hands-on exercises

1. Run `python scripts/check_retrieval.py` — expect **10/10 PASS**.
2. Edit `docs/faqs/refunds.txt`, run `rag_index.py`, ask a refund question again.
3. Run `eval_compare.py -o compare_results.md` and compare `tuned_rag` vs `base_only` for one question.

Details: [docs/LEARNING.md](docs/LEARNING.md)

## Architecture

```text
User question
   → embed (Ollama nomic-embed-text)
   → retrieve top FAQ from ChromaDB
   → prompt with FAQ context
   → generate (MLX Llama 3.2 1B + LoRA adapter)
   → answer
```

Tune first so behavior is stable; add RAG second for factual grounding from `docs/faqs/`.

## FAQ documents

| File | Topics |
|------|--------|
| `refunds.txt` | Annual refund window |
| `billing.txt` | Invoices, billing email, plan changes |
| `passwords.txt` | Password reset |
| `trial_extensions.txt` | Trial extension, teammate limit |
| `account_setup.txt` | Sign-up and verification |
| `cancellation.txt` | Cancel, read-only period, data deletion |
| `team_permissions.txt` | Invites, roles, permissions |
| `support.txt` | How to contact support |

## Support this project

This repo is **free for learning**. If it helped you, consider starring the repo, sharing it, or sponsoring future docs and videos (add your link here when ready).

## Disclaimer

Educational lab software only—not production customer-support or legal advice. All AcornDesk content is fictional.

## License

- **This repository:** MIT — see [LICENSE](LICENSE).
- **Dependencies:** Review licenses for [MLX](https://github.com/ml-explore/mlx), [mlx-lm](https://github.com/ml-explore/mlx-lm), the [Llama base model](https://huggingface.co/mlx-community/Llama-3.2-1B-Instruct-4bit), and Ollama models before redistributing.