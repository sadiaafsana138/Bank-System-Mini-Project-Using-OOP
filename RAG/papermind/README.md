# PaperMind

Upload PDFs and ask questions. Answers come only from your documents.

## How It Works

1. Upload one or more PDF files
2. Ask a question in the chat
3. PaperMind finds the most relevant parts of your documents
4. Groq Llama 3.3 70B generates a grounded answer

## Setup

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file:
```
GROQ_API_KEY=your_key_here
```

Get a free key at: https://console.groq.com

## Run Locally

```bash
streamlit run app.py
```

## Stack

- Streamlit — UI
- PyPDF2 — PDF text extraction
- Sentence Transformers — embeddings
- NumPy — vector similarity search
- Groq Llama 3.3 70B — answer generation
