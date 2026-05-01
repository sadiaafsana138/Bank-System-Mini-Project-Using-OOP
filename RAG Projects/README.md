# 🧠 RAG Master Cheatsheet

> **Retrieval-Augmented Generation** — from PDF ingestion to production patterns  
> Stack: `Groq API` · `FAISS / ChromaDB` · `LangChain` · `HuggingFace Embeddings`

---

## 📖 What's Inside

This notebook is a complete reference for building RAG systems — written for someone who has already built a PDF Q&A project and wants to go deeper into advanced patterns, optimizations, and evaluation.

| Section | Topics |
|---|---|
| 1. Pipeline Overview | End-to-end flow, key terminology |
| 2. PDF Ingestion & Chunking | Fixed, recursive, semantic, sliding window strategies |
| 3. Embeddings | Model comparison, cosine similarity |
| 4. Local Vector DB | FAISS & ChromaDB — build, save, load, filter |
| 5. Retrieval Strategies | Dense, MMR, Hybrid (BM25 + dense), Multi-query |
| 6. Groq API | Direct client, LangChain integration, full LCEL chain |
| 7. Advanced RAG Patterns | Query rewriting, reranking, contextual compression, parent-child chunking, conversational memory |
| 8. Evaluation Metrics | RAGAS, MRR, faithfulness scoring |
| 9. Production Optimizations | Embedding cache, async parallel calls, streaming |
| 10. Failure Modes & Fixes | 8 common problems, hallucination guard, table extraction |

---

## ⚙️ Setup

```bash
pip install groq langchain langchain-community langchain-groq
pip install faiss-cpu chromadb sentence-transformers
pip install pypdf pdfplumber tiktoken rank_bm25
pip install ragas datasets tqdm
```

Set your Groq API key:

```bash
export GROQ_API_KEY="gsk_your_key_here"
```

Get a free key at → [console.groq.com](https://console.groq.com)

---

## 🚀 Quick Start (Minimal RAG in ~20 lines)

```python
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain_groq import ChatGroq
from langchain.chains import RetrievalQA

docs     = PyPDFLoader("doc.pdf").load()
chunks   = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50).split_documents(docs)
embeddings  = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")
vectorstore = FAISS.from_documents(chunks, embeddings)
llm      = ChatGroq(model="llama3-8b-8192", api_key="YOUR_KEY")
qa       = RetrievalQA.from_chain_type(llm=llm, retriever=vectorstore.as_retriever())

print(qa.run("What is this document about?"))
```

---

## 🔑 Key Defaults

| Parameter | Recommended Value |
|---|---|
| Chunk size | 400–600 chars |
| Chunk overlap | 10–15% of chunk size |
| Top-K retrieval | 4–6 chunks |
| Temperature (QA) | `0` or `0.1` |
| Embedding model | `BAAI/bge-small-en-v1.5` |
| Groq model (fast) | `llama3-8b-8192` |
| Groq model (smart) | `llama3-70b-8192` |

---

## 💡 Suggested Projects

### 🟢 Project 0A — Wikipedia RAG *(Beginner — No PDF needed)*

**What:** Instead of a PDF, fetch a Wikipedia article via URL, chunk it, embed it, and answer questions from it. Perfect first step because there's no file handling — just text in, answers out.

**What you'll practice:** Text ingestion without PDF loader, chunking raw text, end-to-end RAG flow with a clean minimal codebase

**Key additions over the cheatsheet quickstart:**
- Fetch article text using `wikipedia` or `requests` library
- Clean the raw text (remove references, citations noise)
- Ask 5 different questions and print answers with scores

```python
import wikipedia

page = wikipedia.page("Transformer (machine learning model)")
text = page.content   # plain text, ready to chunk

# → chunk → embed → FAISS → Groq → answer
Q: "Who introduced the transformer architecture?"
A: "It was introduced by Vaswani et al. at Google Brain in 2017."
```

**Why start here:** Zero file setup, runs in 5 minutes, lets you focus on understanding the RAG loop before worrying about PDF parsing.

---

### 🟢 Project 0B — RAG Flashcard Generator *(Beginner)*

**What:** Feed a PDF (lecture notes, textbook chapter) into RAG and automatically generate Q&A flashcards from it. Output as a CSV you can import into Anki or Notion.

**What you'll practice:** Prompt engineering for generation (not just QA), iterating over chunks, structured LLM output, writing results to file

**Key additions:**
- Iterate over each chunk and prompt Groq to generate 2 flashcards per chunk
- LLM returns JSON: `{"question": "...", "answer": "..."}`
- Collect all cards, deduplicate, save to `flashcards.csv`

```
Input:  lecture_notes.pdf  (20 pages)

Output: flashcards.csv
┌─────────────────────────────────┬──────────────────────────────┐
│ Question                        │ Answer                       │
├─────────────────────────────────┼──────────────────────────────┤
│ What does RAG stand for?        │ Retrieval-Augmented Gen...   │
│ What is chunk overlap used for? │ Preserving context across... │
│ Name 2 local vector databases   │ FAISS and ChromaDB           │
└─────────────────────────────────┴──────────────────────────────┘
```

**Why this project:** Teaches you that RAG isn't only for Q&A — the retriever finds relevant content, the LLM does something useful with it. Changes how you think about what RAG can do.

---

### 🟢 Project 1 — Multi-PDF Research Assistant *(Beginner)*

**What:** Upload multiple PDFs (e.g., research papers, textbooks) and ask questions across all of them at once. The answer includes which document it came from.

**What you'll practice:** Multi-document ingestion, metadata filtering, source citation in answers

**Key additions over your current project:**
- Load a folder of PDFs in a loop
- Add `source` filename to chunk metadata
- Display source document + page number with each answer

```
📁 papers/
  ├── attention_is_all_you_need.pdf
  ├── bert.pdf
  └── gpt3.pdf

Q: "Which paper first introduced positional encoding?"
A: "Positional encoding was introduced in... (Source: attention_is_all_you_need.pdf, p.4)"
```

---

### 🟡 Project 2 — Chat with Your Notes App *(Beginner–Intermediate)*

**What:** A simple Streamlit or Gradio web app where users upload a PDF and chat with it in a multi-turn conversation. Think of it as your own private ChatPDF clone.

**What you'll practice:** Conversational memory, chat UI, session state, streaming responses

**Key additions:**
- `ConversationalRetrievalChain` for multi-turn memory
- Streamlit UI with chat history display
- Groq streaming so responses appear token by token

```
User: What is the document about?
Bot:  It's about transformer architecture...

User: What dataset did they use?       ← references "they" from history
Bot:  They used the WMT 2014 dataset...
```

---

### 🟠 Project 3 — RAG Evaluation Dashboard *(Intermediate)*

**What:** Build a script/notebook that automatically evaluates your RAG pipeline quality using RAGAS. Run it every time you change chunking size, retrieval strategy, or prompt — and compare results in a table.

**What you'll practice:** RAGAS metrics (faithfulness, relevancy, recall, precision), experiment tracking, prompt optimization

**Key additions:**
- Test grid: chunk sizes × retrieval strategies × prompts
- RAGAS scoring for each combination
- Export results to CSV/Excel to compare

```
| chunk_size | retrieval  | faithfulness | answer_relevancy |
|------------|------------|--------------|-----------------|
| 300        | dense      | 0.81         | 0.78            |
| 500        | hybrid     | 0.91         | 0.89  ✅        |
| 800        | mmr        | 0.85         | 0.82            |
```

---

### 🔴 Project 4 — Financial Report Analyzer *(Intermediate–Advanced)*

**What:** Ingest annual reports or earnings PDFs (which have dense tables, charts, and financial data) and answer questions like *"What was the revenue growth from 2022 to 2023?"* accurately.

**What you'll practice:** Table extraction with `pdfplumber`, hybrid retrieval, structured JSON output from LLM, reranking

**Key additions:**
- `pdfplumber` for table-aware PDF parsing
- Hybrid BM25 + dense retrieval (catches exact numbers)
- LLM returns structured JSON: `{ "answer": "...", "figure": "$4.2B", "source_page": 12 }`
- Hallucination guard to verify numbers

```
Q: "What was net income in Q3 2023?"
A: { "answer": "Net income was $2.1B", "confidence": "high", "source_page": 34 }
```

---

### 🔴 Project 5 — Production RAG API with FastAPI *(Advanced)*

**What:** Turn your RAG system into a deployable REST API. Other apps can send a question and get an answer back via HTTP — just like a real product.

**What you'll practice:** FastAPI, async Groq calls, request validation, error handling, Docker containerization, rate limiting

**Endpoints to build:**
```
POST /ingest       → Upload a PDF, returns collection_id
POST /query        → Send question + collection_id, returns answer + sources
GET  /collections  → List all indexed documents
DELETE /collection → Remove an indexed document
```

**Stack:** `FastAPI` + `ChromaDB` (persistent) + `AsyncGroq` + `Docker`

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the paper about?", "collection_id": "abc123"}'
```

---

## 🗺️ Learning Path

```
Your current project
       │
       ▼
[0A] Wikipedia RAG        → no files, understand the loop
       │
       ▼
[0B] Flashcard Generator  → RAG for generation, not just QA
       │
       ▼
[1]  Multi-PDF Assistant  → learn metadata + multi-doc
       │
       ▼
[2]  Chat App (Streamlit) → learn memory + UI
       │
       ▼
[3]  Eval Dashboard       → learn what actually works
       │
       ▼
[4]  Financial Analyzer   → advanced parsing + reranking
       │
       ▼
[5]  Production API       → learn to ship it
```

---

## 📚 Resources

- [Groq Console](https://console.groq.com) — API key + model list
- [LangChain RAG Docs](https://python.langchain.com/docs/use_cases/question_answering/)
- [RAGAS Docs](https://docs.ragas.io) — Evaluation framework
- [FAISS](https://github.com/facebookresearch/faiss) — Facebook's vector search
- [BAAI/bge Models](https://huggingface.co/BAAI) — Best free embedding models

---

*Cheatsheet notebook: `rag_cheatsheet.ipynb`*
