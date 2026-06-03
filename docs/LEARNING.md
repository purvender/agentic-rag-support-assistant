# Learning Guide

This document explains the project in very simple language.

If you are new, read this file slowly from top to bottom.

The goal is to help you understand:

- what this project does,
- what each important AI term means,
- how the pieces connect,
- and what to read next.

---

## One-line idea

This project is a **local support bot**.

It answers customer support questions using:

1. a **small language model**,
2. **LoRA fine-tuning** to improve style,
3. **RAG** to read local FAQ files before answering.

---

## What problem are we solving?

A normal AI model can talk well, but it may guess.

That is dangerous for support use cases because support answers should come from real documents.

So this project teaches the model in **two ways**:

- **LoRA fine-tuning** teaches the model how to sound like a support assistant.
- **RAG** gives the model real FAQ content to answer from.

Simple rule:

- LoRA = **how to talk**
- RAG = **what to talk about**

---

## Big picture

This is the full idea in plain English:

1. A user asks a support question.
2. The system searches local FAQ files.
3. It finds the most relevant text.
4. It adds that text to the prompt.
5. The model writes a support-style answer.

That is the core project.

---

## What is an LLM?

**LLM** means **Large Language Model**.

It is a model trained on lots of text so it can:
- answer questions,
- write text,
- summarize,
- follow instructions.

In this repo, the LLM is the main text generator.

But by itself, it may not know your exact support rules or current policies.

That is why we add fine-tuning and RAG.

---

## What is fine-tuning?

Fine-tuning means taking a base model and training it a little more on your own data.

In this project, the extra data teaches the model to answer like a support assistant.

For example, instead of sounding random or generic, it can learn to sound:
- polite,
- structured,
- clear,
- support-oriented.

Fine-tuning does **not** magically give the model your latest FAQ files.

It mainly improves the **behavior and style** of the answer.

---

## What is LoRA?

**LoRA** means **Low-Rank Adaptation**. It is a parameter-efficient fine-tuning method that keeps the base model weights frozen and learns small trainable updates instead of retraining everything.[web:1360][web:1369]

Simple meaning:

- the original model stays mostly unchanged,
- we train a small adapter,
- that adapter helps the model behave differently.

Why LoRA is useful:

- cheaper than full fine-tuning,
- faster,
- uses less memory,
- easier to run locally.

In this project, LoRA is used so the assistant sounds more like a support bot without needing huge training resources.[web:1360]

---

## What is an embedding?

An **embedding** is a list of numbers that represents the meaning of text. Texts with similar meanings get embeddings that are mathematically close to each other.[web:1361][web:1367]

Simple example:

- “I forgot my password”
- “I can’t log in because I lost my password”

These sentences use different words, but they mean something similar.

Embeddings help the computer notice that similarity.

That is very important for search.

---

## What is a vector database?

A **vector database** stores embeddings and helps find the nearest or most similar ones quickly.[web:1361][web:1364]

In this project, the vector database is **ChromaDB**.

Why we need it:

- FAQ files are split into smaller chunks,
- each chunk gets converted into an embedding,
- those embeddings are stored,
- user questions are also embedded,
- then the system finds the FAQ chunks that are closest in meaning.

That is how semantic search works here.

---

## What is RAG?

**RAG** means **Retrieval-Augmented Generation**. It improves LLM answers by retrieving relevant external information first and then giving that information to the model as context.[web:1358][web:1272][web:1273]

Simple meaning:

1. User asks a question.
2. System searches external knowledge.
3. System adds the found text into the prompt.
4. Model answers using that extra context.

Why this helps:

- better factual grounding,
- less guessing,
- easier to update knowledge by editing documents instead of retraining the model every time.[web:1358][web:1273]

---

## Why not only fine-tuning?

This is one of the most important ideas.

Fine-tuning is good for:
- style,
- format,
- tone,
- behavior.

Fine-tuning is **not** the best tool for:
- frequently changing policies,
- latest product rules,
- editable business knowledge.

If refund policy changes, it is easier to edit a FAQ file than re-train the model.

That is why RAG is so useful.

---

## Why not only RAG?

Because RAG gives facts, but it does not automatically give the best support tone.

A base model with RAG may still:
- sound too generic,
- sound too robotic,
- structure answers poorly.

So this project combines both:

- LoRA for support style,
- RAG for support facts.

That combination is the whole point.

---

## How this project works step by step

Here is the real workflow.

### Step 1: Prepare support training data

Files in `data/support/` contain example prompts and completions.

These examples teach the model what good support answers look like.

### Step 2: Fine-tune with LoRA

The base model is adapted using LoRA training.

This creates adapter weights in:

```text
adapters-llama3-1b/
```

These adapters change the model’s behavior without replacing the whole model.

### Step 3: Prepare FAQ documents

Files in `docs/faqs/` act as the knowledge base.

These are plain text support documents such as:
- refunds,
- billing,
- passwords,
- account setup.

### Step 4: Build embeddings and index

`scripts/rag_index.py` reads the FAQ files, chunks them, creates embeddings, and stores them in ChromaDB.

This creates the searchable knowledge layer.

### Step 5: Ask a question

When you run `scripts/rag_query.py`, the system:
- embeds the user question,
- searches ChromaDB,
- retrieves relevant FAQ chunks,
- builds a prompt,
- asks the model to answer.

That is the end-to-end RAG flow.

---

## Plain flow diagram

```text
FAQ files -> embeddings -> ChromaDB

User question
   -> embed question
   -> find similar FAQ chunks
   -> build prompt with retrieved text
   -> send prompt to model
   -> get final answer
```

---

## What is ChromaDB doing here?

ChromaDB is not generating answers.

It is only helping with **retrieval**.

Its job is:
- store vectorized FAQ chunks,
- search for similar chunks,
- return useful context.

The language model still writes the final answer.

So:

- ChromaDB = search memory
- model = answer writer

---

## What is Ollama doing here?

Ollama is used for the **embedding model**.

In this repo, it uses:

```text
nomic-embed-text
```

Its job is to convert text into vectors.

It is not the final answer model in this project.

Its role is:
- embed FAQ chunks,
- embed the user question,
- make similarity search possible.

---

## What is MLX doing here?

MLX is the Apple Silicon-friendly ML stack used to run and fine-tune the model locally.

In this project, MLX and `mlx-lm` help with:
- loading the model,
- generating answers,
- fine-tuning with LoRA.

This makes the project suitable for local experimentation on Apple Silicon.

---

## What files matter most?

If you feel lost, start with these.

### `scripts/rag_index.py`
This builds the vector database from FAQ files.

Think of it as:
> “Take documents and make them searchable.”

### `scripts/rag_query.py`
This asks the model a question with RAG.

Think of it as:
> “Search relevant docs, then answer.”

### `scripts/eval_compare.py`
This compares different modes:
- base only,
- tuned only,
- base + RAG,
- tuned + RAG.

Think of it as:
> “Which setup works better?”

### `scripts/check_retrieval.py`
This checks whether retrieval is bringing back the right FAQ content.

Think of it as:
> “Is the search part working properly?”

---

## What are the four modes?

This repo compares four setups.

### 1. Base only
Only the base model answers.

No fine-tuning.  
No RAG.

This is the weakest knowledge-grounded mode.

### 2. Tuned only
The fine-tuned LoRA model answers.

Better style, but still no external document retrieval.

### 3. Base + RAG
The base model answers using retrieved FAQ context.

Better factual grounding, but support tone may be weaker.

### 4. Tuned + RAG
The fine-tuned model answers using retrieved FAQ context.

This is usually the strongest setup in this project because it combines:
- support style,
- support facts.

---

## What does “local” mean here?

Local means the main workflow runs on your own machine.

That is useful for:
- learning,
- privacy,
- experiments,
- avoiding cloud costs.

In this project:
- the model runs locally,
- the vector DB is local,
- the FAQ files are local,
- the embeddings are created locally through Ollama.

---

## What does “grounded” mean?

Grounded means the answer is based on real supporting information.

In this project, grounding comes from the FAQ files.

Without grounding, the model may still sound correct but be wrong.

With grounding, the answer is more likely to match your documents.

---

## Why does retrieval need chunking?

FAQ files are usually too large to treat as one giant block.

So the system splits documents into smaller pieces called **chunks**.

Why chunking helps:

- easier to search,
- more relevant matches,
- less noise in the final prompt.

Then the model sees only the most relevant chunks, not the entire document library.

---

## What is a prompt in this project?

A prompt is the text sent to the model.

In plain RAG, the prompt usually contains:

- system instructions,
- user question,
- retrieved FAQ context.

So the model is told:
- who it is,
- what the user wants,
- what support documents say.

Then it generates the answer.

---

## What is evaluation?

Evaluation means checking whether the system is actually working well.

In this repo, evaluation includes:
- comparing different answer modes,
- checking retrieval quality,
- reviewing generated outputs.

This matters because an answer that “sounds good” is not always correct.

---

## What should a beginner do first?

Follow this order.

### 1. Run indexing

```bash
python scripts/rag_index.py
```

This builds the searchable FAQ database.

### 2. Run a plain RAG query

```bash
python scripts/rag_query.py "Can I get a refund for my annual plan?"
```

This shows the main idea quickly.

### 3. Run retrieval checks

```bash
python scripts/check_retrieval.py
```

This helps you understand whether the right FAQ chunks are coming back.

### 4. Run the comparison script

```bash
python scripts/eval_compare.py -o compare_results.md
```

This helps you compare the value of:
- tuning,
- retrieval,
- and both together.

---

## How to think about the architecture

Use this mental model:

- **FAQ files** = the knowledge
- **embeddings** = meaning as numbers
- **ChromaDB** = similarity search engine
- **LoRA adapters** = support personality/style upgrade
- **LLM** = answer generator
- **RAG** = method that connects search with generation

That is the whole system.

---

## Most important understanding

If you remember only one thing, remember this:

> The model does not need to memorize everything.  
> It can retrieve the right information at runtime.

That is why RAG is powerful.

And if you remember one more thing:

> Fine-tuning changes style.  
> Retrieval changes knowledge access.

That is why this project combines both.

---

## What is planned next?

The next big upgrade is **agentic RAG**.

That means adding a simple decision layer before answering.

Future flow:

```text
question -> detect intent -> choose action -> retrieve / clarify / summarize / escalate -> answer
```

That part is the next step for this repository.

It is **not** the main current implementation yet.

---

## Common beginner confusions

### “Is ChromaDB the model?”
No.

ChromaDB is for vector search.

### “Is Ollama answering the user?”
Not in the main design here.

Ollama is used for embeddings.

### “Is fine-tuning the same as RAG?”
No.

Fine-tuning changes model behavior.  
RAG gives model access to relevant documents.

### “Why not just store everything in the prompt?”
Because that becomes too large, too noisy, and hard to manage.

### “Why use LoRA instead of full fine-tuning?”
Because LoRA is lighter, faster, and cheaper for local adaptation.[web:1360][web:1369]

---

## Suggested reading order in the repo

Read files in this order:

1. `README.md`
2. `docs/LEARNING.md`
3. `docs/faqs/`
4. `scripts/rag_index.py`
5. `scripts/rag_query.py`
6. `scripts/check_retrieval.py`
7. `scripts/eval_compare.py`

This order goes from idea -> documents -> search -> answering -> evaluation.

---

## Mini glossary

### LLM
Large Language Model, the text generator.

### LoRA
A lightweight way to fine-tune a model using small trainable adapters instead of retraining everything.[web:1360]

### Embedding
A numeric representation of text meaning.[web:1361][web:1367]

### Vector database
A database that stores embeddings and finds similar ones quickly.[web:1364][web:1361]

### RAG
A method that retrieves relevant external context before generating the answer.[web:1358][web:1272]

### Chunk
A smaller piece of a document used for indexing and retrieval.

### Grounding
Using real supporting documents to reduce guessing.[web:1273][web:1358]

---

## Final mental picture

Think of the project like this:

- The FAQ files are the **book**.
- The vector database is the **smart index** for the book.
- The model is the **writer**.
- LoRA teaches the writer the **right tone**.
- RAG helps the writer **look up the right page before answering**.

That is this project in the simplest possible form.