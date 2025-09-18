# # # import streamlit as st

# # st.set_page_config(page_title="Multi-Page Labs", page_icon="🔬", layout="centered")

# # # Put Lab 2 first so it opens by default
# # nav = st.navigation([
# #     st.Page("lab2.py", title="Lab 2"),
# #     st.Page("lab1.py", title="Lab 1"),
# # ])

# # nav.run()


# # streamlit_app.py
# import streamlit as st

# st.set_page_config(page_title="Multi-Page Labs", page_icon="🔬", layout="centered")

# nav = st.navigation([
#     st.Page("lab2.py", title="Lab 2 — Weighted PDF Summarizer"),
#     st.Page("lab1.py", title="Lab 1 — Document Buddy"),
# <<<<<<< HEAD
#     st.Page("lab3.py", title="Lab 3 — Chatbot"),   # ✅ new page
# =======
# >>>>>>> 7a22ec9e847bd4a6cf259d5e77afb07559763151
# ])

# nav.run()


import streamlit as st

st.set_page_config(page_title="Multi-Page Labs", page_icon="🔬", layout="centered")

nav = st.navigation([
    st.Page("lab4.py", title="Lab 4 — ChromaDB"),
    st.Page("lab3.py", title="Lab 3 — Chatbot"),
    st.Page("lab2.py", title="Lab 2 — Weighted PDF Summarizer"),
    st.Page("lab1.py", title="Lab 1 — Document Buddy"),
    st.Page("lab3.py", title="Lab 3 — Chatbot"),   # ✅ new page
])

nav.run()
