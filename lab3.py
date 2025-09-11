# # # # lab3.py
# # # import os
# # # import streamlit as st
# # # from openai import OpenAI

# # # # ========================= Helpers =========================
# # # def _get_openai_api_key() -> str | None:
# # #     try:
# # #         return st.secrets["OPENAI_API_KEY"]
# # #     except Exception:
# # #         pass
# # #     try:
# # #         from dotenv import load_dotenv
# # #         load_dotenv()
# # #     except Exception:
# # #         pass
# # #     return os.getenv("OPENAI_API_KEY")

# # # # ========================= App Config =========================
# # # st.set_page_config(page_title="Lab 3 — Chatbot", layout="centered")
# # # st.title("Lab 3 — Chatbot with OpenAI")

# # # api_key = _get_openai_api_key()
# # # if not api_key:
# # #     st.error("OPENAI_API_KEY not found. Add it in Streamlit Secrets or `.env`.")
# # #     st.stop()

# # # client = OpenAI(api_key=api_key)

# # # # ========================= Sidebar =========================
# # # with st.sidebar:
# # #     st.header("Chatbot Settings")
# # #     use_advanced = st.checkbox("Use Advanced Model (GPT-4o)", value=False)
# # #     model = "gpt-4o" if use_advanced else "gpt-4o-mini"
# # #     st.caption(f"Currently using: **{model}**")

# # # # ========================= Chat UI =========================
# # # if "messages" not in st.session_state:
# # #     st.session_state.messages = [
# # #         {"role": "system", "content": "You are a helpful assistant for Lab 3."}
# # #     ]

# # # for msg in st.session_state.messages[1:]:
# # #     with st.chat_message(msg["role"]):
# # #         st.markdown(msg["content"])

# # # if prompt := st.chat_input("Say something..."):
# # #     st.session_state.messages.append({"role": "user", "content": prompt})
# # #     with st.chat_message("user"):
# # #         st.markdown(prompt)

# # #     with st.chat_message("assistant"):
# # #         with st.spinner(f"Thinking with {model}..."):
# # #             try:
# # #                 # Use new Responses API (works across all models)
# # #                 resp = client.responses.create(
# # #                     model=model,
# # #                     input=st.session_state.messages,
# # #                 )
# # #                 reply = resp.output_text
# # #             except Exception as e:
# # #                 reply = f"⚠️ API error: {e}"
# # #             st.markdown(reply)

# # #     st.session_state.messages.append({"role": "assistant", "content": reply})

# # # lab3.py
# # import os
# # import streamlit as st
# # from openai import OpenAI

# # # ========================= Helpers =========================
# # def _get_openai_api_key() -> str | None:
# #     try:
# #         return st.secrets["OPENAI_API_KEY"]
# #     except Exception:
# #         pass
# #     try:
# #         from dotenv import load_dotenv
# #         load_dotenv()
# #     except Exception:
# #         pass
# #     return os.getenv("OPENAI_API_KEY")

# # # ========================= App Config =========================
# # st.set_page_config(page_title="Lab 3 — Chatbot", layout="centered")
# # st.title("Lab 3 — Chatbot with OpenAI")

# # api_key = _get_openai_api_key()
# # if not api_key:
# #     st.error("OPENAI_API_KEY not found. Add it in Streamlit Secrets or `.env`.")
# #     st.stop()

# # client = OpenAI(api_key=api_key)

# # # ========================= Sidebar =========================
# # with st.sidebar:
# #     st.header("Chatbot Settings")

# #     available_models = [
# #         "gpt-4o",
# #         "gpt-4o-mini",
# #         "gpt-4.1",
# #         "gpt-4.1-mini",
# #         "gpt-3.5-turbo",
# #         "gpt-5",
# #         "gpt-5-nano",
# #     ]

# #     model = st.selectbox("Select Model", available_models, index=1)
# #     st.caption(f"Currently using: **{model}**")

# # # ========================= Chat UI =========================
# # if "messages" not in st.session_state:
# #     st.session_state.messages = [
# #         {"role": "system", "content": "You are a helpful assistant for Lab 3."}
# #     ]

# # for msg in st.session_state.messages[1:]:
# #     with st.chat_message(msg["role"]):
# #         st.markdown(msg["content"])

# # if prompt := st.chat_input("Say something..."):
# #     st.session_state.messages.append({"role": "user", "content": prompt})
# #     with st.chat_message("user"):
# #         st.markdown(prompt)

# #     with st.chat_message("assistant"):
# #         with st.spinner(f"Thinking with {model}..."):
# #             try:
# #                 # Using Responses API (new unified endpoint)
# #                 resp = client.responses.create(
# #                     model=model,
# #                     input=st.session_state.messages,
# #                 )
# #                 reply = resp.output_text
# #             except Exception as e:
# #                 reply = f"⚠️ API error: {e}"
# #             st.markdown(reply)

# #     st.session_state.messages.append({"role": "assistant", "content": reply})

# # lab3.py
# import os
# import streamlit as st
# from openai import OpenAI

# # ========================= Helpers =========================
# def _get_openai_api_key() -> str | None:
#     try:
#         return st.secrets["OPENAI_API_KEY"]
#     except Exception:
#         pass
#     try:
#         from dotenv import load_dotenv
#         load_dotenv()
#     except Exception:
#         pass
#     return os.getenv("OPENAI_API_KEY")

# # ========================= App Config =========================
# st.set_page_config(page_title="Lab 3 — Chatbot with Memory", layout="centered")
# st.title("Lab 3 — Chatbot with Memory")

# api_key = _get_openai_api_key()
# if not api_key:
#     st.error("OPENAI_API_KEY not found. Add it in Streamlit Secrets or `.env`.")
#     st.stop()

# client = OpenAI(api_key=api_key)

# # ========================= Sidebar =========================
# with st.sidebar:
#     st.header("Chatbot Settings")

#     available_models = [
#         "gpt-4o",
#         "gpt-4o-mini",
#         "gpt-4.1",
#         "gpt-4.1-mini",
#         "gpt-3.5-turbo",
#         "gpt-5",
#         "gpt-5-nano",
#     ]
#     model = st.selectbox("Select Model", available_models, index=1)
#     st.caption(f"Currently using: **{model}**")

#     if st.button("🗑️ Clear Chat History"):
#         st.session_state.messages = [
#             {"role": "system", "content": "You are a helpful assistant for Lab 3."}
#         ]
#         st.rerun()

# # ========================= Initialize Memory =========================
# if "messages" not in st.session_state:
#     st.session_state.messages = [
#         {"role": "system", "content": "You are a helpful assistant for Lab 3."}
#     ]

# # ========================= Render Chat History =========================
# for msg in st.session_state.messages[1:]:  # skip system prompt
#     with st.chat_message(msg["role"]):
#         st.markdown(msg["content"])

# # ========================= Handle User Input =========================
# if prompt := st.chat_input("Say something..."):
#     # Save user input
#     st.session_state.messages.append({"role": "user", "content": prompt})
#     with st.chat_message("user"):
#         st.markdown(prompt)

#     # Generate assistant reply
#     with st.chat_message("assistant"):
#         with st.spinner(f"Thinking with {model}..."):
#             try:
#                 resp = client.responses.create(
#                     model=model,
#                     input=st.session_state.messages,  # full history
#                 )
#                 reply = resp.output_text
#             except Exception as e:
#                 reply = f"⚠️ API error: {e}"
#             st.markdown(reply)

#     # Save assistant reply
#     st.session_state.messages.append({"role": "assistant", "content": reply})


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
st.set_page_config(page_title="Lab 3 — Streaming Chatbot", layout="centered")
st.title("Lab 3 — Streaming Chatbot (with Conversation Buffer)")

api_key = _get_openai_api_key()
if not api_key:
    st.error("OPENAI_API_KEY not found. Add it in Streamlit Secrets or `.env`.")
    st.stop()

client = OpenAI(api_key=api_key)

# ========================= Sidebar =========================
with st.sidebar:
    st.header("Chatbot Settings")

    available_models = [
        "gpt-4o",
        "gpt-4o-mini",
        "gpt-4.1",
        "gpt-4.1-mini",
        "gpt-3.5-turbo",
        "gpt-5",
        "gpt-5-nano",
    ]
    model = st.selectbox("Select Model", available_models, index=1)
    st.caption(f"Currently using: **{model}**")

    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# ========================= Initialize Memory =========================
if "messages" not in st.session_state:
    st.session_state.messages = []  # store user+assistant pairs

# ========================= Render Chat History =========================
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ========================= Handle User Input =========================
if prompt := st.chat_input("Say something..."):
    # Save user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Keep only last 2 user+assistant exchanges
    # Each "exchange" = 1 user + 1 assistant message
    buffer = []
    u_count = 0
    for msg in reversed(st.session_state.messages):
        buffer.insert(0, msg)
        if msg["role"] == "user":
            u_count += 1
            if u_count == 2:
                break

    # Add a system instruction at the start
    messages = [{"role": "system", "content": "You are a helpful assistant."}] + buffer

    # Streaming assistant reply
    with st.chat_message("assistant"):
        st.markdown("⏳ Thinking...")
        placeholder = st.empty()
        reply = ""

        try:
            stream = client.chat.completions.create(
                model=model,
                messages=messages,
                stream=True,
            )
            for chunk in stream:
                delta = chunk.choices[0].delta.content or ""
                reply += delta
                placeholder.markdown(reply)
        except Exception as e:
            reply = f"⚠️ API error: {e}"
            placeholder.markdown(reply)

    # Save assistant reply
    st.session_state.messages.append({"role": "assistant", "content": reply})
