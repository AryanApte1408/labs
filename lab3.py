# lab3.py
import os
import streamlit as st
from openai import OpenAI

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

# ========================= App Config =========================
st.set_page_config(page_title="Lab 3 — Chatbot", layout="centered")
st.title("Lab 3 — Chatbot with OpenAI")

api_key = _get_openai_api_key()
if not api_key:
    st.error("OPENAI_API_KEY not found. Add it in Streamlit Secrets or `.env`.")
    st.stop()

client = OpenAI(api_key=api_key)

# ========================= Sidebar =========================
with st.sidebar:
    st.header("Chatbot Settings")
    use_advanced = st.checkbox("Use Advanced Model (GPT-4o)", value=False)
    model = "gpt-4o" if use_advanced else "gpt-4o-mini"
    st.caption(f"Currently using: **{model}**")

# ========================= Chat UI =========================
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful assistant for Lab 3."}
    ]

for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Say something..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner(f"Thinking with {model}..."):
            try:
                # Use new Responses API (works across all models)
                resp = client.responses.create(
                    model=model,
                    input=st.session_state.messages,
                )
                reply = resp.output_text
            except Exception as e:
                reply = f"⚠️ API error: {e}"
            st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})
