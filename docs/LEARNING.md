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

**RAG** means **Retrieval-Augmented Generation**.

Simple meaning:

1. Read the user question.
2. Search the knowledge base.
3. Pick the most relevant text.
4. Put that text into the prompt.
5. Let the model answer using that context.

That helps the model answer using **real project documents** instead of only guessing from training.

---

## What is agentic RAG?

**Agentic RAG** means adding a small decision-making layer on top of standard RAG.

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

### Core features

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

Before using this project, make sure you already have:

- **macOS**
- **Apple Silicon**
- **Python 3.9+**
- **Git**
- **Ollama** installed locally

---

## First-time setup

Follow these steps in order.

### Step 0 — Install Ollama

Ollama can be installed on macOS either by downloading the app or by using the install script.

Option A — download the macOS app:

- https://ollama.com/download/mac

Option B — install from terminal:

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

After installing, open the Ollama app once so the local service starts.

You can check that the CLI is available with:

```bash
ollama
```

If you see the Ollama interface or help output, the CLI is installed correctly.

### Step 1 — Clone the repository

```bash
git clone https://github.com/purvender/apple-silicon-agentic-rag-support-assistant.git
cd apple-silicon-agentic-rag-support-assistant
```

### Step 2 — Create a Python virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3 — Install Python dependencies

```bash
pip install -r requirements.txt
```

### Step 4 — Pull the embedding model for Ollama

```bash
ollama pull nomic-embed-text
```

### Step 5 — Verify the Ollama model is available

```bash
ollama list
```

You should see `nomic-embed-text` in the list.

### Step 6 — Pre-cache the base MLX model

```bash
python -m mlx_lm generate \
  --model mlx-community/Llama-3.2-1B-Instruct-4bit \
  --prompt "hi" \
  --max-tokens 1
```

This downloads and warms up the base model once so later runs are smoother.

### Step 7 — Build the vector index

```bash
python scripts/rag_index.py
```

This reads the FAQ files, creates embeddings, and stores them in ChromaDB.

### Step 8 — Run a plain RAG query

```bash
python scripts/rag_query.py "Can I get a refund for my annual plan?"
```

### Step 9 — Run the agent workflow

```bash
python scripts/agent_chat.py "I did not receive my password reset email"
```

### Step 10 — Run quick checks

```bash
bash scripts/smoke_test.sh
python scripts/eval_agent.py
```

---

## Quick start summary

If you just want the shortest working path, use these commands:

```bash
git clone https://github.com/purvender/apple-silicon-agentic-rag-support-assistant.git
cd apple-silicon-agentic-rag-support-assistant

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

ollama pull nomic-embed-text
ollama list

python -m mlx_lm generate \
  --model mlx-community/Llama-3.2-1B-Instruct-4bit \
  --prompt "hi" \
  --max-tokens 1

python scripts/rag_index.py
python scripts/rag_query.py "Can I get a refund for my annual plan?"
python scripts/agent_chat.py "I did not receive my password reset email"
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

- learn the flow
- try the project quickly
- inspect the outputs
- understand the architecture first

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

## Learning path

This repository is easiest to understand if you run it in this order:

### Stage 1 — Understand the base model

Learn how the base model answers without retrieval.

### Stage 2 — Understand the tuned model

Learn how LoRA changes style and support tone.

### Stage 3 — Understand RAG

Learn how document retrieval improves factual grounding.

### Stage 4 — Understand tuned RAG

Learn how style + retrieval work together.

### Stage 5 — Understand agentic RAG

Learn how the system decides what to do before answering.

This order helps you understand each layer one by one instead of mixing everything at once.

---

## End-to-end examples

This section shows the same support problem in different modes so you can clearly see what each layer adds.

These are **teaching examples**. Actual outputs may vary slightly.

---

### 1. Base model only

This is the raw base model without LoRA and without RAG.

**User query**

```text
Can I get a refund for my annual plan?
```

**Flow**

```text
User query -> base model answers from general knowledge
```

**What this mode is good for**

- understanding the baseline
- seeing how the untuned model behaves

**Expected behavior**

- may sound generic
- may not follow your support style
- may not know your exact refund rules

**Example answer**

```text
Refund eligibility depends on the company policy and your purchase terms. You may need to review the billing policy or contact support for exact annual plan refund details.
```

---

### 2. Tuned model only

This uses the LoRA-tuned model, but still no RAG.

**User query**

```text
Can I get a refund for my annual plan?
```

**Flow**

```text
User query -> tuned model answers using learned support tone
```

**What this mode is good for**

- seeing the effect of fine-tuning
- checking support tone and structure

**Expected behavior**

- sounds more polite and support-oriented
- still may not know the exact policy unless it saw similar examples during training

**Example answer**

```text
I can help with that. Refunds for annual plans usually depend on the refund window and billing terms. Please review your refund policy or contact support if you need the exact next step for your account.
```

---

### 3. RAG with base model

This uses retrieval, but not the tuned LoRA adapter.

**User query**

```text
Can I get a refund for my annual plan?
```

**Flow**

```text
User query -> embed query -> search ChromaDB -> retrieve refund FAQ -> base model answers with context
```

**What this mode is good for**

- seeing the value of retrieval
- checking whether the right document is found

**Expected behavior**

- more factually grounded
- style may still be plain or generic

**Example retrieved topic**

```text
refunds.txt
```

**Example answer**

```text
According to the refund FAQ, annual plans can be refunded only within the allowed refund window. If you are outside that period, the annual plan is usually non-refundable.
```

---

### 4. RAG with tuned model

This combines retrieval with the LoRA-tuned support style.

**User query**

```text
Can I get a refund for my annual plan?
```

**Flow**

```text
User query -> embed query -> search ChromaDB -> retrieve refund FAQ -> tuned model answers with context
```

**What this mode is good for**

- best non-agent baseline
- combines support tone and factual grounding

**Expected behavior**

- clearer structure
- support-friendly tone
- more accurate document-based answer

**Example answer**

```text
I checked the refund guidance for annual plans. If your purchase is still within the refund window, you may be eligible for a refund. If the refund window has passed, the annual plan is usually non-refundable. Please review your billing date and refund terms before contacting support.
```

---

### 5. Agentic RAG with tuned model

This is the upgraded mode with simple decision-making before the answer.

**User query**

```text
I tried resetting my password twice and still did not get the email.
```

**Flow**

```text
User query
-> classify intent
-> choose tool
-> retrieve password reset FAQ
-> decide response path
-> tuned model drafts final answer
```

**Example intent**

```text
troubleshooting
```

**Example tool path**

```text
retrieve_kb(query) -> draft_final_response(context)
```

**What this mode is good for**

- understanding the agent layer
- routing different request types
- handling support workflows more naturally

**Expected behavior**

- identifies this as a troubleshooting issue
- retrieves the relevant password FAQ
- gives a step-by-step support answer
- may escalate if the issue continues

**Example answer**

```text
This looks like a password reset delivery issue. First, check your spam or promotions folder and confirm you are using the correct account email. If the reset email still does not arrive after retrying, contact support so the account can be checked manually.
```

---

## Why these examples matter

These five examples teach the project step by step:

1. **Base model** shows the raw starting point.
2. **Tuned model** shows tone improvement.
3. **RAG + base** shows factual grounding.
4. **RAG + tuned** shows the best standard support flow.
5. **Agentic RAG + tuned** shows decision-making on top of retrieval.

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

## Why we use fine-tuning, RAG, and agentic RAG

Each layer solves a different problem.

| Layer | What it improves |
|------|-------------------|
| Fine-tuning | Tone, structure, support style |
| RAG | Factual grounding from editable documents |
| Agentic workflow | Choosing the next action before answering |

Simple rule:

- **Fine-tuning** teaches the model **how to answer**
- **RAG** provides the content for **what to answer**
- **Agentic workflow** decides **what to do next**

That is the learning progression of this repository.

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

## Usage

### Plain RAG usage

Ask a support question:

```bash
python scripts/rag_query.py "Can I cancel my plan and still access my data?"
```

Use this mode if you want:

- the simplest system
- direct RAG behavior
- easy debugging

### Agent usage

Ask a support question through the agent layer:

```bash
python scripts/agent_chat.py "I tried resetting my password twice and still didn't get the email."
```

Use this mode if you want:

- intent detection
- routing
- summarization
- basic escalation behavior
- more realistic support workflows

---

## Evaluation

### Four-mode comparison

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

### Retrieval-only check

This checks retrieval quality quickly without full generation:

```bash
python scripts/check_retrieval.py
```

### Agent evaluation

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

If you are new, use this order.

### Step 1 — Start Ollama

```bash
ollama pull nomic-embed-text
ollama list
```

### Step 2 — Build the vector index

```bash
python scripts/rag_index.py
```

### Step 3 — Run plain RAG

```bash
python scripts/rag_query.py "Can I get a refund for my annual plan?"
```

### Step 4 — Compare answer quality

Read the examples in **End-to-end examples** and compare:

- base model
- tuned model
- base + RAG
- tuned + RAG
- agentic RAG + tuned model

### Step 5 — Run the agent

```bash
python scripts/agent_chat.py "I want to talk to a human about my billing issue."
```

### Step 6 — Read code in this order

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