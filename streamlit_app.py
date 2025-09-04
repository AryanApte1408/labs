import streamlit as st

st.set_page_config(page_title="Multi-Page Labs", page_icon="🔬", layout="centered")

st.title("Multi-Page Lab App")

# Redirect to Lab 2 by default when the app first loads
if "sent_default_redirect" not in st.session_state:
    st.session_state.sent_default_redirect = True
    try:
        st.switch_page("pages/2_lab2.py")
    except Exception:
        st.info("Use the sidebar to open Lab 2 if the auto-redirect didn’t work.")

# Links to pages (still useful if redirect fails)
try:
    st.page_link("pages/1_lab1.py", label="Open Lab 1")
    st.page_link("pages/2_lab2.py", label="Open Lab 2 (default)")
except Exception:
    pass
