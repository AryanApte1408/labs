import os
import streamlit as st
from openai import OpenAI

# --- API key: secrets first, then .env/OS env as fallback ---
def _get_openai_api_key() -> str | None:
    # 1) Streamlit Secrets (recommended for deployment)
    try:
        key = st.secrets["OPENAI_API_KEY"]
        if key:
            return key
    except Exception:
        pass

    # 2) .env or environment variable
    #    Optional: load .env if python-dotenv is installed; ignore if not.
    try:
        from dotenv import load_dotenv  # type: ignore
        load_dotenv()
    except Exception:
        pass

    return os.getenv("OPENAI_API_KEY")

api_key = _get_openai_api_key()
if not api_key:
    st.error(
        "OPENAI_API_KEY not found. Add it to **Secrets** (Streamlit Cloud) as "
        "`OPENAI_API_KEY` or set it in a local `.env`/environment variable. "
        "Then rerun the app."
    )
    st.stop()

client = OpenAI(api_key=api_key)

# --- UI ---
st.title("Document Buddy — Lab 2")
st.caption("✅ Using a secure API key from secrets / environment (no text input).")

uploaded_file = st.file_uploader("Upload a document (.txt or .md)", type=("txt", "md"))

question = st.text_area(
    "Now ask a question about the document!",
    placeholder="Summarize the key points in 3 bullets.",
    disabled=not uploaded_file,
)

# --- Inference ---
if uploaded_file and question:
    document = uploaded_file.read().decode()
    messages = [{
        "role": "user",
        "content": f"Here's a document: {document}\n\n---\n\n{question}"
    }]

    stream = client.chat.completions.create(
        model="gpt-4.1",
        messages=messages,
        stream=True,
    )
    st.write_stream(stream)
