import streamlit as st

st.set_page_config(page_title="Multi-Page Labs", page_icon="🔬", layout="centered")

# Put Lab 2 first so it opens by default
nav = st.navigation([
    st.Page("lab2.py", title="Lab 2"),
    st.Page("lab1.py", title="Lab 1"),
])

nav.run()
