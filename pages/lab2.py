import streamlit as st
from openai import OpenAI

# Title for Lab 2
st.title("Document Buddy — Lab 2")
st.caption("✅ You are viewing the second lab page (set as default).")

# Input OpenAI API key
openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:
    client = OpenAI(api_key=openai_api_key)

    # File uploader
    uploaded_file = st.file_uploader("Upload a document (.txt or .md)", type=("txt", "md"))

    # Question input
    question = st.text_area(
        "Now ask a question about the document!",
        placeholder="Summarize the key points in 3 bullets.",
        disabled=not uploaded_file,
    )

    # Process
    if uploaded_file and question:
        document = uploaded_file.read().decode()
        messages = [{"role": "user", "content": f"Here's a document: {document}\n\n---\n\n{question}"}]

        # GPT response
        stream = client.chat.completions.create(
            model="gpt-4.1",
            messages=messages,
            stream=True,
        )
        st.write_stream(stream)
