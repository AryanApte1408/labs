# streamlit_app.py
import streamlit as st

st.set_page_config(page_title="Multi-Page Labs", page_icon="🔬", layout="centered")

# Navigation across all Labs
nav = st.navigation([
    st.Page("lab4.py", title="Lab 4 — ChromaDB"),
    st.Page("lab3.py", title="Lab 3 — Chatbot"),
    st.Page("lab2.py", title="Lab 2 — Weighted PDF Summarizer"),
    st.Page("lab1.py", title="Lab 1 — Document Buddy"),
])

nav.run()
