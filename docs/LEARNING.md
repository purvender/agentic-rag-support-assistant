# Apple Silicon Agentic RAG Support Assistant

A local, beginner-friendly customer support assistant for macOS Apple Silicon using:

- **MLX LoRA fine-tuning**
- **Ollama embeddings**
- **ChromaDB**
- **RAG (Retrieval-Augmented Generation)**
- a simple **agent orchestration layer**

This project shows how to build a support bot that can answer questions from local FAQ files, speak in a support-friendly tone, and gradually grow from a plain RAG bot into a small **agentic RAG** system.

---

## What this project is

This repository is a learning project and implementation guide for a **local support assistant**.

It runs fully on-device on **Apple Silicon Mac** and demonstrates three important ideas:

1. **Fine-tuning** for response style and tone  
2. **RAG** for factual grounding from local documents  
3. **Agentic workflow** for simple decision-making before answering  

In simple words:

- the model learns **how to talk** using LoRA fine-tuning,
- the system learns **what to answer** using FAQ retrieval,
- the agent layer learns **what to do next** using routing and tools.

---

## Why this project exists

A plain LLM can sound fluent, but it may guess or hallucinate.

A plain RAG system is better because it retrieves real documents before answering.

An **agentic RAG** system goes one step further:
- it can detect what kind of request the user has,
- choose the right tool,
- ask for clarification,
- summarize the conversation,
- or escalate to a human path when needed.

This repository is designed so a beginner can understand that journey step by step.

---

## What is RAG?

**RAG** means **Retrieval-Augmented Generation**.[web:1314]

Simple meaning:

1. Read user question  
2. Search the knowledge base  
3. Pick the most relevant text  
4. Put that text into the prompt  
5. Let the model answer using that context  

That helps the model answer using **real project documents** instead of only guessing from training.

---

## What is agentic RAG?

**Agentic RAG** means we add a small decision-making layer on top of RAG.[web:1319]

Instead of always doing only this:

```text
question -> retrieve docs -> generate answer
```

the system can do this:

```text
question -> classify intent -> choose tool(s) -> retrieve / summarize / escalate / clarify -> generate answer
```

In this project, the agent layer is intentionally simple and beginner-friendly:
- one Python orchestrator
- small tools
- lightweight memory/state
- clear file structure

This is **not** a complex multi-agent system.  
It is a practical first step into agentic AI.

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

### Agentic features

- intent classification
- simple tool-based workflow
- lightweight conversation state
- summarization support
- escalation stub
- evaluation scenarios for agent behavior

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
  - agentic orchestration
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
| Agent layer | simple Python orchestration |

---

## Project idea in one sentence

This project builds a **fictional AcornDesk support assistant** that answers from local FAQ documents, speaks in a support tone, and evolves from plain RAG into a small agentic RAG workflow.

---

## What is included in the repo

Everything below is included so a new user can clone and run the project quickly:

| Included | Location | Purpose |
|----------|----------|---------|
| Pre-trained LoRA adapters | `adapters-llama3-1b/` | Run the tuned model immediately |
| Training data | `data/support/*.jsonl` | Re-train or study the fine-tuning format |
| FAQ documents | `docs/faqs/*.txt` | Knowledge base for retrieval |
| Eval prompts | `data/eval/test_prompts.txt` | Four-mode evaluation |
| Agent scenarios | `data/eval/agent_scenarios.json` | Agent behavior tests |
| Scripts | `scripts/` | Index, query, evaluate |
| Agent code | `agent/` | Routing, tools, memory, orchestration |

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
git clone https://github.com/purvender/apple-silicon-agentic-rag-support-assistant.git
cd apple-silicon-agentic-rag-support-assistant
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

### 5. Ask a question with the agent workflow

```bash
python scripts/agent_chat.py "I did not receive my password reset email"
```

### 6. Run quick checks

```bash
bash scripts/smoke_test.sh
python scripts/eval_agent.py
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
python scripts/agent_chat.py "I forgot my password and the reset email is not coming."
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

## How the agentic layer works

This is the upgraded flow:

```text
User question
   -> classify the intent
   -> choose which tool to use
   -> maybe retrieve FAQ context
   -> maybe summarize the conversation
   -> maybe ask for clarification
   -> maybe escalate
   -> draft final response
```

### Example intents

The system can classify a question as:

- `knowledge_base`
- `troubleshooting`
- `policy_process`
- `escalation`
- `summarization`
- `unknown`

### Example tools

The simple Python agent can call tools like:

- `retrieve_kb(query)`
- `classify_intent(query, history)`
- `summarize_conversation(history)`
- `search_similar_issues(query)`
- `escalate_to_human(reason, summary)`
- `draft_final_response(context)`

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

The agent layer adds:
- **what to do next**

---

## Project structure

```text
apple-silicon-agentic-rag-support-assistant/
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
│       ├── expected_sources.jsonl
│       └── agent_scenarios.json
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
├── agent/
│   ├── __init__.py
│   ├── types.py
│   ├── memory.py
│   ├── prompts.py
│   ├── router.py
│   ├── tools.py
│   └── orchestrator.py
├── scripts/
│   ├── mlx_utils.py
│   ├── rag_index.py
│   ├── rag_query.py
│   ├── agent_chat.py
│   ├── eval_compare.py
│   ├── eval_agent.py
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
Runs the original plain RAG assistant.

### `scripts/agent_chat.py`
Runs the upgraded agentic workflow.

### `scripts/eval_compare.py`
Compares base vs tuned vs RAG combinations.

### `scripts/eval_agent.py`
Runs simple tests for the agent flow.

### `agent/router.py`
Decides what kind of request the user has.

### `agent/tools.py`
Contains the small tool functions the agent can call.

### `agent/memory.py`
Stores lightweight conversation state.

### `agent/orchestrator.py`
Main controller for the agent workflow.

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

## Agent usage

Ask a support question through the agent layer:

```bash
python scripts/agent_chat.py "I tried resetting my password twice and still didn't get the email."
```

Use this mode if you want:
- intent detection,
- routing,
- summarization,
- basic escalation behavior,
- more realistic support workflows.

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

## Agent evaluation

This checks whether the agent chooses the expected intent for simple scenarios:

```bash
python scripts/eval_agent.py
```

Example scenario types:
- FAQ question
- troubleshooting issue
- escalation request
- summary request

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
Run the agent:

```bash
python scripts/agent_chat.py "I want to talk to a human about my billing issue."
```

### Step 5
Read these files in this order:

1. `scripts/rag_index.py`
2. `scripts/rag_query.py`
3. `agent/router.py`
4. `agent/tools.py`
5. `agent/orchestrator.py`

That order makes the architecture easier to understand.

---

## What changed from the original repo

Originally, this project was mainly a **local LoRA + RAG support assistant**.

Now it is being upgraded into a **local agentic RAG support assistant**.

### Old version
- retrieve FAQ
- answer using retrieved context

### New version
- understand request type
- choose next action
- retrieve / summarize / escalate / clarify
- then answer

This is the key evolution in the repository.

---

## Limitations

This project is intentionally small and beginner-friendly.

Current limitations:

- fictional support domain only
- simple local documents only
- lightweight agent logic
- no real ticketing backend
- no production authentication or web UI
- escalation is a stub, not a real helpdesk integration
- retrieval is intentionally simple for learning clarity

---

## Future improvements

Possible next steps:

- persistent conversation memory
- better retrieval ranking
- real issue history search
- real ticket system integration
- web UI or API layer
- LangGraph migration for larger workflows
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