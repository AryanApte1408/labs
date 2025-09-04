import streamlit as st

st.set_page_config(page_title="Multi-Page Labs", page_icon="🔬", layout="centered")

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Lab 1", "Lab 2"], index=1)  # Default = Lab 2

if page == "Lab 1":
    st.switch_page("pages/1_lab1.py")
else:
    st.switch_page("pages/2_lab2.py")
