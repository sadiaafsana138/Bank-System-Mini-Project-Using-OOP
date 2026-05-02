# 🧠 RAG Complete Cheatsheet — Beginner to Expert

> **Stack**: Groq API · FAISS / ChromaDB · LangChain · HuggingFace Embeddings  
> **Covers**: Everything from "what is RAG" to production-grade systems

---

## 📋 What's Inside — 33 Sections, 104 Cells

### 🟢 Beginner (Sections 1–10)

| # | Section | What you learn |
|---|---|---|
| 1 | What is RAG & Why it Exists | Problem with plain LLMs, RAG vs fine-tuning, key vocabulary |
| 2 | Setup & Installation | All packages, API key setup, .env file usage |
| 3 | Your First RAG in 20 Lines | Full pipeline, RAG from plain text (no PDF needed) |
| 4 | Loading Documents | PDF, TXT, URLs, Wikipedia, CSV, entire folders |
| 5 | Chunking | RecursiveSplitter, token-based, metadata, visual debugger |
| 6 | Embeddings | HuggingFace models, cosine similarity explained with numbers |
| 7 | Vector DBs — FAISS & ChromaDB | Build, save, load, add new docs, basic search |
| 8 | Retrieval Basics | Retriever setup, formatting context for LLM |
| 9 | Groq API & Generation | Direct API, LCEL chain, model comparison table |
| 10 | Prompt Engineering | Bad vs good vs structured prompts, JSON output parsing |

### 🟡 Intermediate (Sections 11–16)

| # | Section | What you learn |
|---|---|---|
| 11 | Advanced Chunking | Semantic chunking, parent-child, sliding window |
| 12 | Advanced Retrieval | MMR, BM25 hybrid, multi-query retrieval |
| 13 | Conversational RAG | All 3 memory types, ConversationalRetrievalChain |
| 14 | Metadata Filtering | ChromaDB filter syntax, self-querying retriever |
| 15 | Tables, Images & Scanned PDFs | pdfplumber table extraction, OCR with Unstructured |
| 16 | Query Rewriting & HyDE | Rewriting vague queries, Hypothetical Document Embedding |

### 🔴 Advanced (Sections 17–22)

| # | Section | What you learn |
|---|---|---|
| 17 | Reranking | Cross-encoder reranker, contextual compression |
| 18 | Advanced Architectures | Corrective RAG (CRAG), chunk summarization, agentic RAG |
| 19 | Evaluation (RAGAS) | Faithfulness, relevancy, precision, recall, MRR, A/B testing |
| 20 | Production Optimizations | Embedding cache, async batch, streaming, retry logic |
| 21 | FastAPI RAG API | Full REST API: /ingest, /query, /collections endpoints |
| 22 | Failures & Debugging | Debug mode, hallucination guard, failure mode table |

### 🟣 Expert (Sections 24–33)

| # | Section | What you learn |
|---|---|---|
| 24 | Document Preprocessing | Text cleaning pipeline, deduplication, header-aware chunking |
| 25 | LangGraph | RAG as a state machine, conditional branching, retry loops |
| 26 | Multi-modal RAG | Extract images from PDFs, describe with vision LLM, index both |
| 27 | GraphRAG | Build knowledge graphs, entity extraction, relationship-based retrieval |
| 28 | Observability & Tracing | LangSmith setup, custom query logger, token cost estimator |
| 29 | Vector DB at Scale | HNSW, IVF, PQ indexes, when to move to Qdrant/Pinecone |
| 30 | Re-ingestion Strategy | Partial updates, change detection, smart_ingest() |
| 31 | Security | Prompt injection scanner, jailbreak patterns, API key safety |
| 32 | Code-Aware Chunking | Language-aware splitters, mixed doc routing |
| 33 | Complete Quick Reference | Decision guide, key numbers, full dependency list, all resources |

---

## ⚙️ Setup

```bash
# Core
pip install groq langchain langchain-community langchain-groq langchain-experimental

# Vector DBs
pip install faiss-cpu chromadb

# Embeddings & Reranking
pip install sentence-transformers

# Document Loading
pip install pypdf pdfplumber pymupdf unstructured[pdf]

# Retrieval Utilities
pip install rank_bm25 tiktoken

# Evaluation
pip install ragas datasets

# Graphs & Agentic
pip install langgraph networkx

# API & Serving
pip install fastapi uvicorn python-dotenv

# Observability
pip install langsmith
```

Set your Groq API key (free at [console.groq.com](https://console.groq.com)):

```bash
export GROQ_API_KEY="gsk_your_key_here"
```

---

## 🚀 Quick Start — Minimal RAG in 15 Lines

```python
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain_groq import ChatGroq
from langchain.chains import RetrievalQA

docs  = PyPDFLoader("doc.pdf").load()
chunks= RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50).split_documents(docs)
vs    = FAISS.from_documents(chunks, HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5"))
qa    = RetrievalQA.from_chain_type(llm=ChatGroq(model="llama3-8b-8192"), retriever=vs.as_retriever())
print(qa.run("What is this document about?"))
```

---

## 🗺️ Decision Guide — When to Use What

```
Just starting?               → Dense + bge-small + FAISS
Exact terms / IDs matter?    → Add BM25 hybrid retrieval
Duplicate answers?           → MMR retrieval
Vague user questions?        → Query rewriting or multi-query
Dense technical doc?         → Parent-child chunking
Multi-hop reasoning needed?  → LangGraph + Corrective RAG
Relationships between ideas? → GraphRAG
Images / charts in PDF?      → Multi-modal (vision LLM descriptions)
PDF has tables?              → pdfplumber
Scanned / image PDF?         → Unstructured + OCR
Doc contains code?           → Language-aware code splitter
Doc updates frequently?      → Chroma + smart_ingest() change detection
LLM hallucinating?           → Stronger prompt + faithfulness guard
Can't debug failures?        → LangSmith tracing + custom query logger
Scaling past 100K chunks?    → Qdrant / Pinecone + IVF index
Building an API?             → FastAPI + ChromaDB
Security concerns?           → Injection scanner + env vars
Multi-turn chat?             → ConversationalRetrievalChain + memory
Need to measure quality?     → RAGAS evaluation
Tracking costs?              → Token cost estimator (Section 28)
```

---

## 🔑 Key Numbers at a Glance

| Parameter | Default | Production Notes |
|---|---|---|
| Chunk size | 500 chars | Tune with RAGAS — don't guess |
| Chunk overlap | 50 chars | 10–15% of chunk size |
| Top-K chunks | 4 | 6–8 for complex questions |
| Temperature | 0 | 0 = factual, 0.3 = creative |
| MMR fetch_k | 20 | 5× your final K |
| Reranker pool | 20 | Retrieve 20, rerank → pass top 4 |
| Max context | < 60% of context window | Leave room for system prompt |
| Faithfulness target | > 0.85 | Below → fix prompt or retrieval |
| FAISS safe limit | ~100K chunks | Above: use IVF index or Qdrant |

---

## 💡 Project Ideas — Beginner to Advanced

### 🟢 Project 0A — Wikipedia RAG *(No files needed)*
Fetch a Wikipedia article, chunk it, answer questions. Runs in 5 minutes.  
**Goal**: Understand the core loop without any file complexity.

### 🟢 Project 0B — Flashcard Generator
Feed lecture notes → auto-generate Q&A flashcards → export CSV for Anki/Notion.  
**Goal**: RAG for generation, not just answering questions.

### 🟢 Project 1 — Multi-PDF Research Assistant
Ask questions across multiple PDFs with source citation.  
**New skills**: Multi-doc ingestion, metadata filtering.

### 🟡 Project 2 — Chat with Notes App (Streamlit)
Upload a PDF, chat with it in multi-turn conversation.  
**New skills**: ConversationalRetrievalChain, Streamlit UI, streaming.

### 🟠 Project 3 — RAG Evaluation Dashboard
Test every config change (chunk size, retrieval strategy, prompt) and compare scores.  
**New skills**: RAGAS metrics, experiment tracking.

### 🔴 Project 4 — Financial Report Analyzer
Answer questions about tables and numbers in annual reports accurately.  
**New skills**: pdfplumber, hybrid retrieval, structured JSON output.

### 🔴 Project 5 — Production RAG API (FastAPI)
REST API: upload PDFs and query them over HTTP.  
**New skills**: FastAPI, async Groq, Docker-ready.

---

## 🛤️ Learning Path

```
Your current project (PDF Q&A)
         │
         ▼
[0A] Wikipedia RAG         → understand the loop, no file setup
         │
         ▼
[0B] Flashcard Generator   → RAG for generation, not just Q&A
         │
         ▼
[1]  Multi-PDF Assistant   → metadata, multi-doc, source citation
         │
         ▼
[2]  Chat App (Streamlit)  → memory, UI, streaming
         │
         ▼
[3]  Eval Dashboard        → measure what actually works
         │
         ▼
[4]  Financial Analyzer    → tables, reranking, structured output
         │
         ▼
[5]  Production API        → ship it as a real service
```

---

## 📚 All Resources

| Resource | What for |
|---|---|
| [console.groq.com](https://console.groq.com) | Free Groq API key |
| [python.langchain.com](https://python.langchain.com) | LangChain RAG docs |
| [langchain-ai.github.io/langgraph](https://langchain-ai.github.io/langgraph) | LangGraph docs |
| [smith.langchain.com](https://smith.langchain.com) | LangSmith tracing (free) |
| [docs.ragas.io](https://docs.ragas.io) | RAGAS evaluation framework |
| [huggingface.co/BAAI](https://huggingface.co/BAAI) | Best free embedding models |
| [github.com/facebookresearch/faiss](https://github.com/facebookresearch/faiss) | FAISS vector search |
| [docs.trychroma.com](https://docs.trychroma.com) | ChromaDB docs |
| [qdrant.tech](https://qdrant.tech) | Qdrant (scale beyond FAISS) |
| [github.com/microsoft/graphrag](https://github.com/microsoft/graphrag) | Microsoft GraphRAG |
| [unstructured.io](https://unstructured.io) | OCR + table extraction |

---

*Notebook: `rag_cheatsheet.ipynb` · 33 sections · 104 cells · Beginner → Expert*  
*Stack: Groq API · FAISS / ChromaDB · LangChain · LangGraph · HuggingFace*
