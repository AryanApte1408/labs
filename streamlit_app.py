import streamlit as st

st.set_page_config(page_title="Multi-Page Labs", page_icon="🔬", layout="centered")

nav = st.navigation([
    st.Page("lab2.py", title="Lab 2 — Weighted PDF Summarizer"),
    st.Page("lab1.py", title="Lab 1 — Document Buddy"),
])

nav.run()
