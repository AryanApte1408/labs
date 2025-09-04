import streamlit as st
from openai import OpenAI

st.title("Document Buddy — Lab 1")
st.write(
    "Upload a document below and ask a question about it – GPT will answer! "
    "To use this app, provide an OpenAI API key from https://platform.openai.com/account/api-keys."
)

openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:
    client = OpenAI(api_key=openai_api_key)

    uploaded_file = st.file_uploader("Upload a document (.txt or .md)", type=("txt", "md"))
    question = st.text_area(
        "Now ask a question about the document!",
        placeholder="Can you give me a short summary?",
        disabled=not uploaded_file,
    )

    if uploaded_file and question:
        document = uploaded_file.read().decode()
        messages = [{"role": "user", "content": f"Here's a document: {document}\n\n---\n\n{question}"}]

        stream = client.chat.completions.create(
            model="gpt-4.1",
            messages=messages,
            stream=True,
        )
        st.write_stream(stream)
