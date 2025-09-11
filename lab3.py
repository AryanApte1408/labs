# lab3.py
import os
import streamlit as st
from openai import OpenAI

# ========================= Helpers =========================
def _get_openai_api_key() -> str | None:
    # 1) Streamlit Cloud secrets
    try:
        key = st.secrets["OPENAI_API_KEY"]
        if key:
            return key
    except Exception:
        pass
    # 2) Local .env fallback
    try:
        from dotenv import load_dotenv  # type: ignore
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

# Show previous messages
for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input box
if prompt := st.chat_input("Say something..."):
    # Store user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get assistant reply
    with st.chat_message("assistant"):
        with st.spinner(f"Thinking with {model}..."):
            resp = client.chat.completions.create(
                model=model,
                messages=st.session_state.messages,
            )
            reply = resp.choices[0].message.content
            st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})
