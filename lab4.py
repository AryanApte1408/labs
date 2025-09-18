# lab4.py — Lab 4: Build & Test a ChromaDB Collection
import os
import streamlit as st
from openai import OpenAI
import fitz  # PyMuPDF
import chromadb
from chromadb.utils import embedding_functions
import streamlit as st
from openai import OpenAI
import os
from PyPDF2 import PdfReader

# --- Fix for ChromaDB + Streamlit Cloud ---
__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import chromadb

# ========================= Helpers =========================
def _get_openai_api_key() -> str | None:
    try:
        return st.secrets["OPENAI_API_KEY"]
    except Exception:
        pass
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except Exception:
        pass
    return os.getenv("OPENAI_API_KEY")

def read_pdf(path: str) -> str:
    """Extract text from a PDF using PyMuPDF."""
    text = []
    with fitz.open(path) as doc:
        for page in doc:
            text.append(page.get_text() or "")
    return "\n".join(text)

# ========================= Build ChromaDB =========================
def build_chroma_from_pdfs(pdf_folder: str, persist_dir: str):
    """Build a ChromaDB collection from PDFs (only once per run)."""
    api_key = _get_openai_api_key()
    if not api_key:
        st.error("OPENAI_API_KEY not found. Add it to Streamlit Secrets or `.env`.")
        st.stop()

    # Persistent client
    client = chromadb.PersistentClient(path=persist_dir)

    # OpenAI embedding function
    embed_fn = embedding_functions.OpenAIEmbeddingFunction(
        api_key=api_key,
        model_name="text-embedding-3-small"
    )

    # Create / get collection
    collection = client.get_or_create_collection(
        name="Lab4Collection",
        embedding_function=embed_fn
    )

    # If collection already has documents, skip adding
    if collection.count() > 0:
        return collection

    # Load PDFs
    pdf_files = [os.path.join(pdf_folder, f) for f in os.listdir(pdf_folder) if f.endswith(".pdf")]
    for path in pdf_files:
        text = read_pdf(path)
        if not text.strip():
            continue
        fname = os.path.basename(path)
        collection.add(
            documents=[text],
            ids=[fname],
            metadatas=[{"filename": fname}]
        )
        st.write(f"✅ Added {fname} to Lab4Collection")

    return collection

# ========================= App Config =========================
st.set_page_config(page_title="Lab 4 — ChromaDB", layout="centered")
st.title("Lab 4 — Build & Test a ChromaDB Collection")

# ========================= Initialize =========================
PDF_FOLDER = r"D:\Syracuse\HC-AI\labs\lab4_docs"
PERSIST_DIR = os.path.join(PDF_FOLDER, "chroma_store")

if "Lab4_vectorDB" not in st.session_state:
    st.session_state.Lab4_vectorDB = build_chroma_from_pdfs(PDF_FOLDER, PERSIST_DIR)
    st.success("Lab4Collection is ready and stored in session.")

collection = st.session_state.Lab4_vectorDB

# ========================= Test Queries =========================
st.header("Test Search")
queries = ["Generative AI", "Text Mining", "Data Science Overview"]

for q in queries:
    st.subheader(f"🔎 Query: {q}")
    results = collection.query(query_texts=[q], n_results=3)
    if results and results["metadatas"]:
        files = [m["filename"] for m in results["metadatas"][0]]
        st.write("Top matches:", files)
    else:
        st.warning("No results found.")
