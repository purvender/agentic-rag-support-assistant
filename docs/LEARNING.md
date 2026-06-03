# Learning Guide

This file explains the project as a step-by-step learning journey.

The goal is not only to run the code, but also to understand what each layer adds:

1. base model
2. tuned model
3. RAG
4. tuned RAG
5. agentic RAG

If you are new to local AI systems, read this file after `README.md`.

---

## What you are building

This project builds a **fictional AcornDesk support assistant**.

The assistant answers support questions using local FAQ documents and runs fully on-device on **Apple Silicon Mac**.

The project teaches three main ideas:

- **Fine-tuning** changes how the model speaks
- **RAG** changes what knowledge the model can access
- **Agentic workflow** changes what the system does before answering

---

## Big picture

This project is easiest to understand as five stages.

### Stage 1 — Base model only

The raw base model answers from its general training.

It may sound fluent, but it does not know your exact support policies.

Use this stage to understand the baseline.

### Stage 2 — Tuned model only

The LoRA-tuned model is trained on support-style examples.

It becomes more polite, more structured, and more consistent in support tone.

But it still may not know the exact contents of your local FAQ files.

### Stage 3 — RAG with retrieval

The system now searches your FAQ documents before answering.

This gives the model access to local, editable knowledge.

This is where factual grounding starts.

### Stage 4 — Tuned RAG

This combines the best parts of Stage 2 and Stage 3.

The assistant now has both:

- support tone
- document grounding

For many beginner projects, this is the most useful standard setup.

### Stage 5 — Agentic RAG

The system adds a simple reasoning layer before answering.

Now it can do things like:

- detect whether a question is troubleshooting or policy related
- choose retrieval
- summarize context
- ask for clarification
- escalate when needed

This makes the system feel more like a real support workflow.

---

## Core concepts

## Fine-tuning

Fine-tuning changes the model’s behavior.

In this project, LoRA fine-tuning teaches the model:

- support-friendly tone
- concise response style
- consistent structure
- customer-safe wording

A useful way to remember it:

> Fine-tuning teaches the model **how to answer**.

---

## Embeddings

Embeddings convert text into vectors.

Those vectors let the system compare user questions with FAQ documents based on semantic similarity.

That means the system can find related text even if the wording is different.

Example:

- user asks: `I forgot my password`
- FAQ may say: `reset your account credentials`

Embeddings help connect those as similar meaning.

---

## Vector search

After embeddings are created, they are stored in **ChromaDB**.

When the user asks a question:

1. the question is embedded
2. ChromaDB searches for similar document chunks
3. the most relevant chunks are returned

This is the retrieval step.

---

## RAG

RAG stands for **Retrieval-Augmented Generation**.

That means:

1. retrieve the relevant document text
2. put it into the model prompt
3. generate an answer using that context

A useful way to remember it:

> RAG provides **what to answer**.

---

## Agentic RAG

Agentic RAG adds a simple decision layer before the answer is generated.

Instead of always doing the same retrieve-then-answer flow, the system can first decide what kind of request it is.

Example:

- policy question -> retrieve FAQ
- troubleshooting question -> retrieve troubleshooting info
- escalation request -> summarize and escalate
- summary request -> summarize conversation history

A useful way to remember it:

> Agentic RAG decides **what to do next**.

---

## How to study this repository

Read the code in this order.

### 1. `scripts/rag_index.py`

This script builds the vector index from the FAQ files.

Study this file to understand:

- where the FAQ files come from
- how documents are loaded
- how embeddings are generated
- how ChromaDB is populated

### 2. `scripts/rag_query.py`

This script runs the plain RAG assistant.

Study this file to understand:

- how a user query is processed
- how relevant FAQ content is retrieved
- how the final prompt is built
- how the answer is generated

### 3. `agent/router.py`

This file classifies the user request into an intent.

Study this file to understand:

- how the system distinguishes question types
- how the agent decides whether something is knowledge, troubleshooting, escalation, or summary

### 4. `agent/tools.py`

This file contains the callable tools the agent can use.

Study this file to understand:

- which actions exist
- how retrieval, summarization, or escalation are modeled
- how simple tool abstractions make the workflow easier to extend

### 5. `agent/orchestrator.py`

This file is the controller for the full agentic workflow.

Study this file to understand:

- how the agent combines router + tools + memory
- how the final answer path is selected
- where the system becomes agentic

### 6. `agent/memory.py`

This file stores lightweight conversation state.

Study this file to understand:

- how multi-step support behavior can be made more consistent
- how history is passed into routing or summarization

---

## How to run the project while learning

Follow this order.

### Step 1 — Install Ollama and dependencies

Use the `README.md` setup section first.

Important reminder:

- install Ollama
- clone the repo
- create the virtual environment
- install `requirements.txt`
- pull `nomic-embed-text`

### Step 2 — Build the vector index

```bash
python scripts/rag_index.py
```

What to observe:

- the FAQ files are read
- embeddings are created
- ChromaDB is populated locally

### Step 3 — Run plain RAG

```bash
python scripts/rag_query.py "Can I get a refund for my annual plan?"
```

What to observe:

- the system retrieves FAQ content
- the final answer should reference the refund rules from your local docs

### Step 4 — Inspect retrieval quality

```bash
python scripts/check_retrieval.py
```

What to observe:

- whether the right FAQ files are being retrieved
- whether the top matches make sense for the question

### Step 5 — Run the agent

```bash
python scripts/agent_chat.py "I tried resetting my password twice and still didn't get the email."
```

What to observe:

- whether the query is treated as troubleshooting
- whether the agent follows a more structured support workflow
- whether escalation or clarification logic is triggered

### Step 6 — Run evaluations

```bash
python scripts/eval_compare.py -o compare_results.md
python scripts/eval_agent.py
```

What to observe:

- quality differences across base, tuned, and RAG modes
- whether the agent chooses the expected intent path

---

## Comparing the five modes

Use the same question to compare behavior.

Recommended test question:

```text
Can I get a refund for my annual plan?
```

### Mode 1 — Base model

Expected behavior:

- generic answer
- no guarantee of project-specific policy accuracy

### Mode 2 — Tuned model

Expected behavior:

- better tone
- still limited factual grounding

### Mode 3 — RAG with base model

Expected behavior:

- better facts
- weaker tone than tuned model

### Mode 4 — RAG with tuned model

Expected behavior:

- better facts
- better tone
- best standard support answer

### Mode 5 — Agentic RAG with tuned model

Recommended second test question:

```text
I tried resetting my password twice and still did not get the email.
```

Expected behavior:

- classify as troubleshooting
- retrieve relevant FAQ or support instructions
- produce a more procedural answer
- escalate when needed

---

## What a beginner should learn from this project

By the end of this project, you should understand:

- why fine-tuning and RAG are different
- why RAG is better than relying only on model memory for policy answers
- why vector databases are useful
- why an agent layer is not the same as retrieval
- how a small local AI system can be structured clearly

---

## Common beginner misunderstandings

### “Fine-tuning gives the model new knowledge”

Not necessarily.

Fine-tuning is better for behavior, structure, and style.

If the knowledge changes often, RAG is usually the better choice.

### “RAG replaces fine-tuning”

Not always.

RAG helps with current facts and editable knowledge.

Fine-tuning helps with tone and response style.

They solve different problems.

### “Agentic RAG means a huge multi-agent system”

No.

In this project, agentic RAG is intentionally simple.

It means a small decision layer with tools and routing before the final answer.

### “If retrieval works, the answer is automatically perfect”

Not always.

Good retrieval helps, but prompt construction, response formatting, and fallback logic still matter.

---

## Good experiments to try

Try these learning experiments.

### Experiment 1 — Edit an FAQ file

Change something in one of the files under `docs/faqs/`.

Then rebuild the index:

```bash
python scripts/rag_index.py
```

Ask the related question again.

This teaches you that RAG can update behavior through documents without retraining the model.

### Experiment 2 — Improve the support tone

Edit the training examples in `data/support/`.

Then re-run LoRA fine-tuning.

This teaches you that fine-tuning changes style and response behavior.

### Experiment 3 — Add a new intent

Extend the router with a new intent class.

Then add a new tool path in the orchestrator.

This teaches you how an agent system grows over time.

### Experiment 4 — Compare output side by side

Use the same question in:

- base
- tuned
- RAG
- agentic RAG

Then note:

- which answer is most accurate
- which answer is most helpful
- which answer sounds most support-friendly

---

## Recommended reading order

1. `README.md`
2. `docs/LEARNING.md`
3. `scripts/rag_index.py`
4. `scripts/rag_query.py`
5. `agent/router.py`
6. `agent/tools.py`
7. `agent/orchestrator.py`
8. `docs/TROUBLESHOOTING.md`

---

## Final mindset

The best way to learn this repository is to treat it as a progression:

- first understand the model
- then understand retrieval
- then understand orchestration

Do not try to understand everything at once.

Run one script, inspect one file, and learn one layer at a time.