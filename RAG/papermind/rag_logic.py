import io
import os
import re
import numpy as np
from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
model = SentenceTransformer("all-MiniLM-L6-v2")


def read_pdf(file_bytes):
    pdf_stream = io.BytesIO(file_bytes)
    reader = PdfReader(pdf_stream)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + " "
    cleaned = re.sub(r"\s+", " ", text).strip()
    return cleaned


def split_text(text, chunk_size=400, overlap=100):
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        if end >= len(words):
            break
        start = end - overlap
    return chunks


def embed_texts(texts):
    embeddings = model.encode(texts, convert_to_numpy=True, show_progress_bar=False)
    for i in range(len(embeddings)):
        norm = np.linalg.norm(embeddings[i])
        if norm > 0:
            embeddings[i] = embeddings[i] / norm
    return embeddings


def build_vector_store(uploaded_files, chunk_size=400, overlap=100):
    chunks = []
    sources = []
    for uploaded_file in uploaded_files:
        text = read_pdf(uploaded_file.read())
        file_chunks = split_text(text, chunk_size, overlap)
        for index, chunk in enumerate(file_chunks, start=1):
            chunks.append(chunk)
            sources.append(f"{uploaded_file.name} chunk {index}")
    if not chunks:
        return {"chunks": [], "embeddings": [], "sources": []}
    embeddings = embed_texts(chunks)
    return {"chunks": chunks, "embeddings": embeddings, "sources": sources}


def find_similar_chunks(question, store, top_k=4):
    if not store["chunks"]:
        return []
    question_embedding = embed_texts([question])[0]
    scores = store["embeddings"] @ question_embedding
    top_indexes = np.argsort(-scores)[:top_k]
    results = []
    for index in top_indexes:
        results.append({
            "text": store["chunks"][index],
            "source": store["sources"][index],
            "score": float(scores[index]),
        })
    return results


def ask_groq(question, retrieved):
    context = ""
    for item in retrieved:
        context += f"Source: {item['source']}\n{item['text']}\n\n---\n\n"

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "Answer questions using ONLY the provided context. If the answer is not in the context, say so."
            },
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion: {question}"
            }
        ],
        temperature=0.2,
        max_tokens=1000,
    )
    return response.choices[0].message.content