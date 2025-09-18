# # # lab4.py — Lab 4: Build & Test a ChromaDB Collection
# # import os
# # import streamlit as st
# # from openai import OpenAI
# # import fitz  # PyMuPDF
# # import chromadb
# # from chromadb.utils import embedding_functions
# # import streamlit as st
# # from openai import OpenAI
# # import os
# # from PyPDF2 import PdfReader

# # # --- Fix for ChromaDB + Streamlit Cloud ---
# # __import__('pysqlite3')
# # import sys
# # sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

# # import chromadb

# # # ========================= Helpers =========================
# # def _get_openai_api_key() -> str | None:
# #     try:
# #         return st.secrets["OPENAI_API_KEY"]
# #     except Exception:
# #         pass
# #     try:
# #         from dotenv import load_dotenv
# #         load_dotenv()
# #     except Exception:
# #         pass
# #     return os.getenv("OPENAI_API_KEY")

# # def read_pdf(path: str) -> str:
# #     """Extract text from a PDF using PyMuPDF."""
# #     text = []
# #     with fitz.open(path) as doc:
# #         for page in doc:
# #             text.append(page.get_text() or "")
# #     return "\n".join(text)

# # # ========================= Build ChromaDB =========================
# # def build_chroma_from_pdfs(pdf_folder: str, persist_dir: str):
# #     """Build a ChromaDB collection from PDFs (only once per run)."""
# #     api_key = _get_openai_api_key()
# #     if not api_key:
# #         st.error("OPENAI_API_KEY not found. Add it to Streamlit Secrets or `.env`.")
# #         st.stop()

# #     # Persistent client
# #     client = chromadb.PersistentClient(path=persist_dir)

# #     # OpenAI embedding function
# #     embed_fn = embedding_functions.OpenAIEmbeddingFunction(
# #         api_key=api_key,
# #         model_name="text-embedding-3-small"
# #     )

# #     # Create / get collection
# #     collection = client.get_or_create_collection(
# #         name="Lab4Collection",
# #         embedding_function=embed_fn
# #     )

# #     # If collection already has documents, skip adding
# #     if collection.count() > 0:
# #         return collection

# #     # Load PDFs
# #     pdf_files = [os.path.join(pdf_folder, f) for f in os.listdir(pdf_folder) if f.endswith(".pdf")]
# #     for path in pdf_files:
# #         text = read_pdf(path)
# #         if not text.strip():
# #             continue
# #         fname = os.path.basename(path)
# #         collection.add(
# #             documents=[text],
# #             ids=[fname],
# #             metadatas=[{"filename": fname}]
# #         )
# #         st.write(f"✅ Added {fname} to Lab4Collection")

# #     return collection

# # # ========================= App Config =========================
# # st.set_page_config(page_title="Lab 4 — ChromaDB", layout="centered")
# # st.title("Lab 4 — Build & Test a ChromaDB Collection")

# # # ========================= Initialize =========================
# # PDF_FOLDER = r"D:\Syracuse\HC-AI\labs\lab4_docs"
# # PERSIST_DIR = os.path.join(PDF_FOLDER, "chroma_store")

# # if "Lab4_vectorDB" not in st.session_state:
# #     st.session_state.Lab4_vectorDB = build_chroma_from_pdfs(PDF_FOLDER, PERSIST_DIR)
# #     st.success("Lab4Collection is ready and stored in session.")

# # collection = st.session_state.Lab4_vectorDB

# # # ========================= Test Queries =========================
# # st.header("Test Search")
# # queries = ["Generative AI", "Text Mining", "Data Science Overview"]

# # for q in queries:
# #     st.subheader(f"🔎 Query: {q}")
# #     results = collection.query(query_texts=[q], n_results=3)
# #     if results and results["metadatas"]:
# #         files = [m["filename"] for m in results["metadatas"][0]]
# #         st.write("Top matches:", files)
# #     else:
# #         st.warning("No results found.")

# # lab4.py — Lab 4: Build & Test a ChromaDB Collection
# import os
# import sys
# import streamlit as st
# import fitz  # PyMuPDF
# import chromadb
# from chromadb.utils import embedding_functions
# from openai import OpenAI

# # --- Fix for ChromaDB + Streamlit Cloud (SQLite versioning) ---
# __import__('pysqlite3')
# sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')


# # ========================= Helpers =========================
# def _get_openai_api_key() -> str | None:
#     try:
#         return st.secrets["OPENAI_API_KEY"]
#     except Exception:
#         pass
#     try:
#         from dotenv import load_dotenv
#         load_dotenv()
#     except Exception:
#         pass
#     return os.getenv("OPENAI_API_KEY")


# def read_pdf(path: str) -> str:
#     """Extract text from a PDF using PyMuPDF."""
#     text = []
#     with fitz.open(path) as doc:
#         for page in doc:
#             text.append(page.get_text() or "")
#     return "\n".join(text)


# # ========================= Build ChromaDB =========================
# def build_chroma_from_pdfs(pdf_folder: str, persist_dir: str):
#     """Build a ChromaDB collection from PDFs (only once per run)."""
#     api_key = _get_openai_api_key()
#     if not api_key:
#         st.error("OPENAI_API_KEY not found. Add it to Streamlit Secrets or `.env`.")
#         st.stop()

#     # Persistent client
#     client = chromadb.PersistentClient(path=persist_dir)

#     # OpenAI embedding function
#     embed_fn = embedding_functions.OpenAIEmbeddingFunction(
#         api_key=api_key,
#         model_name="text-embedding-3-small"
#     )

#     # Create / get collection
#     collection = client.get_or_create_collection(
#         name="Lab4Collection",
#         embedding_function=embed_fn
#     )

#     # If collection already has documents, skip adding
#     if collection.count() > 0:
#         return collection

#     # Load PDFs
#     pdf_files = [os.path.join(pdf_folder, f) for f in os.listdir(pdf_folder) if f.endswith(".pdf")]
#     if not pdf_files:
#         st.warning("⚠️ No PDF files found in lab4_docs. Did you upload them to your repo?")
#     for path in pdf_files:
#         text = read_pdf(path)
#         if not text.strip():
#             continue
#         fname = os.path.basename(path)
#         collection.add(
#             documents=[text],
#             ids=[fname],
#             metadatas=[{"filename": fname}]
#         )
#         st.write(f"✅ Added {fname} to Lab4Collection")

#     return collection


# # ========================= App Config =========================
# st.set_page_config(page_title="Lab 4 — ChromaDB", layout="centered")
# st.title("Lab 4 — Build & Test a ChromaDB Collection")

# # ========================= Initialize =========================
# # Use relative path so it works on both local + cloud
# PDF_FOLDER = os.path.join(os.path.dirname(__file__), "lab4_docs")
# PERSIST_DIR = os.path.join(PDF_FOLDER, "chroma_store")

# # Debug info
# st.write("📂 Looking for PDFs in:", PDF_FOLDER)
# if os.path.exists(PDF_FOLDER):
#     st.write("Found files:", os.listdir(PDF_FOLDER))
# else:
#     st.error("❌ PDF folder not found. Make sure `lab4_docs/` exists in your repo.")

# if "Lab4_vectorDB" not in st.session_state:
#     st.session_state.Lab4_vectorDB = build_chroma_from_pdfs(PDF_FOLDER, PERSIST_DIR)
#     st.success("Lab4Collection is ready and stored in session.")

# collection = st.session_state.Lab4_vectorDB

# # ========================= Test Queries =========================
# st.header("Test Search")
# queries = ["Generative AI", "Text Mining", "Data Science Overview"]

# for q in queries:
#     st.subheader(f"🔎 Query: {q}")
#     results = collection.query(query_texts=[q], n_results=3)
#     if results and results["metadatas"]:
#         files = [m["filename"] for m in results["metadatas"][0]]
#         st.write("Top matches:", files)
#     else:
#         st.warning("No results found.")


# lab4.py — Lab 4b: Course Information Chatbot with ChromaDB
import os
import sys
import streamlit as st
import fitz  # PyMuPDF
import chromadb
from chromadb.utils import embedding_functions
from openai import OpenAI

# --- Fix for ChromaDB + Streamlit Cloud (SQLite versioning) ---
__import__('pysqlite3')
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')


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
st.set_page_config(page_title="Lab 4b — Course Chatbot", layout="centered")
st.title("Lab 4b — Course Information Chatbot (RAG with ChromaDB)")

# ========================= Initialize =========================
PDF_FOLDER = os.path.join(os.path.dirname(__file__), "lab4_docs")
PERSIST_DIR = os.path.join(PDF_FOLDER, "chroma_store")

if "Lab4_vectorDB" not in st.session_state:
    st.session_state.Lab4_vectorDB = build_chroma_from_pdfs(PDF_FOLDER, PERSIST_DIR)
    st.success("Lab4Collection is ready and stored in session.")

collection = st.session_state.Lab4_vectorDB

api_key = _get_openai_api_key()
client = OpenAI(api_key=api_key)

# ========================= Chatbot =========================
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "system", "content": "You are a helpful course assistant. "
                                      "Answer questions clearly and simply. "
                                      "If you use knowledge from the course PDFs, say: "
                                      "'This answer uses course materials.'"}
    ]

# Show chat history
for msg in st.session_state.chat_history[1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
if prompt := st.chat_input("Ask me about the course..."):
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Retrieve from ChromaDB
    results = collection.query(query_texts=[prompt], n_results=3)
    docs = []
    if results and results["documents"]:
        docs = results["documents"][0]
    rag_context = "\n\n".join(docs) if docs else "No relevant course material found."

    # Build augmented prompt
    augmented_prompt = (
        f"User question: {prompt}\n\n"
        f"Relevant course material:\n{rag_context}\n\n"
        "Now answer the question clearly for a student. "
        "If you used the course material above, explicitly say: "
        "'This answer uses course materials.'"
    )

    # Get assistant reply
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            resp = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": augmented_prompt}]
            )
            reply = resp.choices[0].message.content
            st.markdown(reply)

    st.session_state.chat_history.append({"role": "assistant", "content": reply})
