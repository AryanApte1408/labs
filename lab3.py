# # # # # # # lab3.py
# # # # # # import os
# # # # # # import streamlit as st
# # # # # # from openai import OpenAI

# # # # # # # ========================= Helpers =========================
# # # # # # def _get_openai_api_key() -> str | None:
# # # # # #     try:
# # # # # #         return st.secrets["OPENAI_API_KEY"]
# # # # # #     except Exception:
# # # # # #         pass
# # # # # #     try:
# # # # # #         from dotenv import load_dotenv
# # # # # #         load_dotenv()
# # # # # #     except Exception:
# # # # # #         pass
# # # # # #     return os.getenv("OPENAI_API_KEY")

# # # # # # # ========================= App Config =========================
# # # # # # st.set_page_config(page_title="Lab 3 — Chatbot", layout="centered")
# # # # # # st.title("Lab 3 — Chatbot with OpenAI")

# # # # # # api_key = _get_openai_api_key()
# # # # # # if not api_key:
# # # # # #     st.error("OPENAI_API_KEY not found. Add it in Streamlit Secrets or `.env`.")
# # # # # #     st.stop()

# # # # # # client = OpenAI(api_key=api_key)

# # # # # # # ========================= Sidebar =========================
# # # # # # with st.sidebar:
# # # # # #     st.header("Chatbot Settings")
# # # # # #     use_advanced = st.checkbox("Use Advanced Model (GPT-4o)", value=False)
# # # # # #     model = "gpt-4o" if use_advanced else "gpt-4o-mini"
# # # # # #     st.caption(f"Currently using: **{model}**")

# # # # # # # ========================= Chat UI =========================
# # # # # # if "messages" not in st.session_state:
# # # # # #     st.session_state.messages = [
# # # # # #         {"role": "system", "content": "You are a helpful assistant for Lab 3."}
# # # # # #     ]

# # # # # # for msg in st.session_state.messages[1:]:
# # # # # #     with st.chat_message(msg["role"]):
# # # # # #         st.markdown(msg["content"])

# # # # # # if prompt := st.chat_input("Say something..."):
# # # # # #     st.session_state.messages.append({"role": "user", "content": prompt})
# # # # # #     with st.chat_message("user"):
# # # # # #         st.markdown(prompt)

# # # # # #     with st.chat_message("assistant"):
# # # # # #         with st.spinner(f"Thinking with {model}..."):
# # # # # #             try:
# # # # # #                 # Use new Responses API (works across all models)
# # # # # #                 resp = client.responses.create(
# # # # # #                     model=model,
# # # # # #                     input=st.session_state.messages,
# # # # # #                 )
# # # # # #                 reply = resp.output_text
# # # # # #             except Exception as e:
# # # # # #                 reply = f"⚠️ API error: {e}"
# # # # # #             st.markdown(reply)

# # # # # #     st.session_state.messages.append({"role": "assistant", "content": reply})

# # # # # # lab3.py
# # # # # import os
# # # # # import streamlit as st
# # # # # from openai import OpenAI

# # # # # # ========================= Helpers =========================
# # # # # def _get_openai_api_key() -> str | None:
# # # # #     try:
# # # # #         return st.secrets["OPENAI_API_KEY"]
# # # # #     except Exception:
# # # # #         pass
# # # # #     try:
# # # # #         from dotenv import load_dotenv
# # # # #         load_dotenv()
# # # # #     except Exception:
# # # # #         pass
# # # # #     return os.getenv("OPENAI_API_KEY")

# # # # # # ========================= App Config =========================
# # # # # st.set_page_config(page_title="Lab 3 — Chatbot", layout="centered")
# # # # # st.title("Lab 3 — Chatbot with OpenAI")

# # # # # api_key = _get_openai_api_key()
# # # # # if not api_key:
# # # # #     st.error("OPENAI_API_KEY not found. Add it in Streamlit Secrets or `.env`.")
# # # # #     st.stop()

# # # # # client = OpenAI(api_key=api_key)

# # # # # # ========================= Sidebar =========================
# # # # # with st.sidebar:
# # # # #     st.header("Chatbot Settings")

# # # # #     available_models = [
# # # # #         "gpt-4o",
# # # # #         "gpt-4o-mini",
# # # # #         "gpt-4.1",
# # # # #         "gpt-4.1-mini",
# # # # #         "gpt-3.5-turbo",
# # # # #         "gpt-5",
# # # # #         "gpt-5-nano",
# # # # #     ]

# # # # #     model = st.selectbox("Select Model", available_models, index=1)
# # # # #     st.caption(f"Currently using: **{model}**")

# # # # # # ========================= Chat UI =========================
# # # # # if "messages" not in st.session_state:
# # # # #     st.session_state.messages = [
# # # # #         {"role": "system", "content": "You are a helpful assistant for Lab 3."}
# # # # #     ]

# # # # # for msg in st.session_state.messages[1:]:
# # # # #     with st.chat_message(msg["role"]):
# # # # #         st.markdown(msg["content"])

# # # # # if prompt := st.chat_input("Say something..."):
# # # # #     st.session_state.messages.append({"role": "user", "content": prompt})
# # # # #     with st.chat_message("user"):
# # # # #         st.markdown(prompt)

# # # # #     with st.chat_message("assistant"):
# # # # #         with st.spinner(f"Thinking with {model}..."):
# # # # #             try:
# # # # #                 # Using Responses API (new unified endpoint)
# # # # #                 resp = client.responses.create(
# # # # #                     model=model,
# # # # #                     input=st.session_state.messages,
# # # # #                 )
# # # # #                 reply = resp.output_text
# # # # #             except Exception as e:
# # # # #                 reply = f"⚠️ API error: {e}"
# # # # #             st.markdown(reply)

# # # # #     st.session_state.messages.append({"role": "assistant", "content": reply})

# # # # # lab3.py
# # # # import os
# # # # import streamlit as st
# # # # from openai import OpenAI

# # # # # ========================= Helpers =========================
# # # # def _get_openai_api_key() -> str | None:
# # # #     try:
# # # #         return st.secrets["OPENAI_API_KEY"]
# # # #     except Exception:
# # # #         pass
# # # #     try:
# # # #         from dotenv import load_dotenv
# # # #         load_dotenv()
# # # #     except Exception:
# # # #         pass
# # # #     return os.getenv("OPENAI_API_KEY")

# # # # # ========================= App Config =========================
# # # # st.set_page_config(page_title="Lab 3 — Chatbot with Memory", layout="centered")
# # # # st.title("Lab 3 — Chatbot with Memory")

# # # # api_key = _get_openai_api_key()
# # # # if not api_key:
# # # #     st.error("OPENAI_API_KEY not found. Add it in Streamlit Secrets or `.env`.")
# # # #     st.stop()

# # # # client = OpenAI(api_key=api_key)

# # # # # ========================= Sidebar =========================
# # # # with st.sidebar:
# # # #     st.header("Chatbot Settings")

# # # #     available_models = [
# # # #         "gpt-4o",
# # # #         "gpt-4o-mini",
# # # #         "gpt-4.1",
# # # #         "gpt-4.1-mini",
# # # #         "gpt-3.5-turbo",
# # # #         "gpt-5",
# # # #         "gpt-5-nano",
# # # #     ]
# # # #     model = st.selectbox("Select Model", available_models, index=1)
# # # #     st.caption(f"Currently using: **{model}**")

# # # #     if st.button("🗑️ Clear Chat History"):
# # # #         st.session_state.messages = [
# # # #             {"role": "system", "content": "You are a helpful assistant for Lab 3."}
# # # #         ]
# # # #         st.rerun()

# # # # # ========================= Initialize Memory =========================
# # # # if "messages" not in st.session_state:
# # # #     st.session_state.messages = [
# # # #         {"role": "system", "content": "You are a helpful assistant for Lab 3."}
# # # #     ]

# # # # # ========================= Render Chat History =========================
# # # # for msg in st.session_state.messages[1:]:  # skip system prompt
# # # #     with st.chat_message(msg["role"]):
# # # #         st.markdown(msg["content"])

# # # # # ========================= Handle User Input =========================
# # # # if prompt := st.chat_input("Say something..."):
# # # #     # Save user input
# # # #     st.session_state.messages.append({"role": "user", "content": prompt})
# # # #     with st.chat_message("user"):
# # # #         st.markdown(prompt)

# # # #     # Generate assistant reply
# # # #     with st.chat_message("assistant"):
# # # #         with st.spinner(f"Thinking with {model}..."):
# # # #             try:
# # # #                 resp = client.responses.create(
# # # #                     model=model,
# # # #                     input=st.session_state.messages,  # full history
# # # #                 )
# # # #                 reply = resp.output_text
# # # #             except Exception as e:
# # # #                 reply = f"⚠️ API error: {e}"
# # # #             st.markdown(reply)

# # # #     # Save assistant reply
# # # #     st.session_state.messages.append({"role": "assistant", "content": reply})


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
# # # st.set_page_config(page_title="Lab 3 — Streaming Chatbot", layout="centered")
# # # st.title("Lab 3 — Streaming Chatbot (with Conversation Buffer)")

# # # api_key = _get_openai_api_key()
# # # if not api_key:
# # #     st.error("OPENAI_API_KEY not found. Add it in Streamlit Secrets or `.env`.")
# # #     st.stop()

# # # client = OpenAI(api_key=api_key)

# # # # ========================= Sidebar =========================
# # # with st.sidebar:
# # #     st.header("Chatbot Settings")

# # #     available_models = [
# # #         "gpt-4o",
# # #         "gpt-4o-mini",
# # #         "gpt-4.1",
# # #         "gpt-4.1-mini",
# # #         "gpt-3.5-turbo",
# # #         "gpt-5",
# # #         "gpt-5-nano",
# # #     ]
# # #     model = st.selectbox("Select Model", available_models, index=1)
# # #     st.caption(f"Currently using: **{model}**")

# # #     if st.button("🗑️ Clear Chat History"):
# # #         st.session_state.messages = []
# # #         st.rerun()

# # # # ========================= Initialize Memory =========================
# # # if "messages" not in st.session_state:
# # #     st.session_state.messages = []  # store user+assistant pairs

# # # # ========================= Render Chat History =========================
# # # for msg in st.session_state.messages:
# # #     with st.chat_message(msg["role"]):
# # #         st.markdown(msg["content"])

# # # # ========================= Handle User Input =========================
# # # if prompt := st.chat_input("Say something..."):
# # #     # Save user message
# # #     st.session_state.messages.append({"role": "user", "content": prompt})
# # #     with st.chat_message("user"):
# # #         st.markdown(prompt)

# # #     # Keep only last 2 user+assistant exchanges
# # #     # Each "exchange" = 1 user + 1 assistant message
# # #     buffer = []
# # #     u_count = 0
# # #     for msg in reversed(st.session_state.messages):
# # #         buffer.insert(0, msg)
# # #         if msg["role"] == "user":
# # #             u_count += 1
# # #             if u_count == 2:
# # #                 break

# # #     # Add a system instruction at the start
# # #     messages = [{"role": "system", "content": "You are a helpful assistant."}] + buffer

# # #     # Streaming assistant reply
# # #     with st.chat_message("assistant"):
# # #         st.markdown("⏳ Thinking...")
# # #         placeholder = st.empty()
# # #         reply = ""

# # #         try:
# # #             stream = client.chat.completions.create(
# # #                 model=model,
# # #                 messages=messages,
# # #                 stream=True,
# # #             )
# # #             for chunk in stream:
# # #                 delta = chunk.choices[0].delta.content or ""
# # #                 reply += delta
# # #                 placeholder.markdown(reply)
# # #         except Exception as e:
# # #             reply = f"⚠️ API error: {e}"
# # #             placeholder.markdown(reply)

# # #     # Save assistant reply
# # #     st.session_state.messages.append({"role": "assistant", "content": reply})


# # # lab3.py
# # import os
# # import streamlit as st
# # from openai import OpenAI
# # import tiktoken

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

# # def count_tokens(messages, model="gpt-4o-mini") -> int:
# #     """Approximate token count for a list of messages."""
# #     try:
# #         enc = tiktoken.encoding_for_model(model)
# #     except Exception:
# #         enc = tiktoken.get_encoding("cl100k_base")  # fallback
# #     total = 0
# #     for msg in messages:
# #         total += len(enc.encode(msg["content"]))
# #     return total

# # def truncate_messages(messages, model, max_tokens: int):
# #     """Keep only as many messages as fit within max_tokens."""
# #     truncated = []
# #     total = 0
# #     # Walk backwards (newest first), keep until budget exceeded
# #     for msg in reversed(messages):
# #         tokens = count_tokens([msg], model)
# #         if total + tokens <= max_tokens:
# #             truncated.insert(0, msg)
# #             total += tokens
# #         else:
# #             break
# #     return truncated

# # # ========================= App Config =========================
# # st.set_page_config(page_title="Lab 3 — Streaming Chatbot (Token Buffer)", layout="centered")
# # st.title("Lab 3 — Streaming Chatbot (Token Buffer)")

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

# #     max_tokens = st.slider("Max tokens to keep in buffer", 500, 4000, 2000, step=100)
# #     st.caption("Chat history will be truncated so total input ≤ this value.")

# #     if st.button("🗑️ Clear Chat History"):
# #         st.session_state.messages = []
# #         st.rerun()

# # # ========================= Initialize Memory =========================
# # if "messages" not in st.session_state:
# #     st.session_state.messages = []

# # # ========================= Render Chat History =========================
# # for msg in st.session_state.messages:
# #     with st.chat_message(msg["role"]):
# #         st.markdown(msg["content"])

# # # ========================= Handle User Input =========================
# # if prompt := st.chat_input("Say something..."):
# #     # Save user message
# #     st.session_state.messages.append({"role": "user", "content": prompt})
# #     with st.chat_message("user"):
# #         st.markdown(prompt)

# #     # Truncate with token budget
# #     buffer = truncate_messages(st.session_state.messages, model, max_tokens)

# #     # Add system prompt
# #     messages = [{"role": "system", "content": "You are a helpful assistant."}] + buffer

# #     # Streaming assistant reply
# #     with st.chat_message("assistant"):
# #         st.markdown("⏳ Thinking...")
# #         placeholder = st.empty()
# #         reply = ""

# #         try:
# #             stream = client.chat.completions.create(
# #                 model=model,
# #                 messages=messages,
# #                 stream=True,
# #             )
# #             for chunk in stream:
# #                 delta = chunk.choices[0].delta.content or ""
# #                 reply += delta
# #                 placeholder.markdown(reply)
# #         except Exception as e:
# #             reply = f"⚠️ API error: {e}"
# #             placeholder.markdown(reply)

# #     # Save assistant reply
# #     st.session_state.messages.append({"role": "assistant", "content": reply})

# #     # Show current buffer token usage
# #     used_tokens = count_tokens(messages, model)
# #     st.sidebar.caption(f"🧮 Tokens sent: {used_tokens} / {max_tokens}")


# # lab3.py — Lab 3c: Refined Chatbot with "More Info" Loop
# import os
# import streamlit as st
# from openai import OpenAI
# import tiktoken

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

# def count_tokens(messages, model="gpt-4o-mini") -> int:
#     try:
#         enc = tiktoken.encoding_for_model(model)
#     except Exception:
#         enc = tiktoken.get_encoding("cl100k_base")
#     total = 0
#     for msg in messages:
#         total += len(enc.encode(msg["content"]))
#     return total

# def truncate_messages(messages, model, max_tokens: int):
#     truncated = []
#     total = 0
#     for msg in reversed(messages):
#         tokens = count_tokens([msg], model)
#         if total + tokens <= max_tokens:
#             truncated.insert(0, msg)
#             total += tokens
#         else:
#             break
#     return truncated

# # ========================= App Config =========================
# st.set_page_config(page_title="Lab 3c — Refined Chatbot", layout="centered")
# st.title("Lab 3c — Refined Chatbot (Token Buffer + More Info Loop)")

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

#     max_tokens = st.slider("Max tokens to keep in buffer", 500, 4000, 2000, step=100)
#     st.caption("Chat history will be truncated so total input ≤ this value.")

#     if st.button("🗑️ Clear Chat History"):
#         st.session_state.messages = []
#         st.session_state.mode = "question"
#         st.rerun()

# # ========================= Initialize State =========================
# if "messages" not in st.session_state:
#     st.session_state.messages = []
# if "mode" not in st.session_state:
#     st.session_state.mode = "question"  # can be "question" or "followup"

# # ========================= Render Chat History =========================
# for msg in st.session_state.messages:
#     with st.chat_message(msg["role"]):
#         st.markdown(msg["content"])

# # ========================= Handle Input =========================
# if prompt := st.chat_input("Type here..."):
#     # Save user input
#     st.session_state.messages.append({"role": "user", "content": prompt})
#     with st.chat_message("user"):
#         st.markdown(prompt)

#     # Decide behavior based on mode
#     if st.session_state.mode == "question":
#         # User asked a new question → answer simply
#         buffer = truncate_messages(st.session_state.messages, model, max_tokens)
#         messages = [{"role": "system", "content": "Explain answers simply so a 10-year-old can understand."}] + buffer

#         with st.chat_message("assistant"):
#             st.markdown("⏳ Thinking...")
#             placeholder = st.empty()
#             reply = ""

#             try:
#                 stream = client.chat.completions.create(
#                     model=model,
#                     messages=messages,
#                     stream=True,
#                 )
#                 for chunk in stream:
#                     delta = chunk.choices[0].delta.content or ""
#                     reply += delta
#                     placeholder.markdown(reply)
#             except Exception as e:
#                 reply = f"⚠️ API error: {e}"
#                 placeholder.markdown(reply)

#         st.session_state.messages.append({"role": "assistant", "content": reply})

#         # Bot asks if user wants more info
#         followup = "Do you want more info?"
#         with st.chat_message("assistant"):
#             st.markdown(followup)
#         st.session_state.messages.append({"role": "assistant", "content": followup})

#         st.session_state.mode = "followup"

#     elif st.session_state.mode == "followup":
#         # If user says yes → expand
#         if prompt.strip().lower() in ["yes", "y", "yeah", "yep", "sure", "ok"]:
#             buffer = truncate_messages(st.session_state.messages, model, max_tokens)
#             messages = [{"role": "system", "content": "Give a deeper explanation, still easy for a 10-year-old to follow."}] + buffer

#             with st.chat_message("assistant"):
#                 st.markdown("⏳ Adding more info...")
#                 placeholder = st.empty()
#                 reply = ""

#                 try:
#                     stream = client.chat.completions.create(
#                         model=model,
#                         messages=messages,
#                         stream=True,
#                     )
#                     for chunk in stream:
#                         delta = chunk.choices[0].delta.content or ""
#                         reply += delta
#                         placeholder.markdown(reply)
#                 except Exception as e:
#                     reply = f"⚠️ API error: {e}"
#                     placeholder.markdown(reply)

#             st.session_state.messages.append({"role": "assistant", "content": reply})

#             # Ask again
#             followup = "Do you want more info?"
#             with st.chat_message("assistant"):
#                 st.markdown(followup)
#             st.session_state.messages.append({"role": "assistant", "content": followup})

#         else:
#             # If user says no → reset to question mode
#             reply = "Okay! What question can I help you with next?"
#             with st.chat_message("assistant"):
#                 st.markdown(reply)
#             st.session_state.messages.append({"role": "assistant", "content": reply})
#             st.session_state.mode = "question"

#     # Show token usage
#     used_tokens = count_tokens(st.session_state.messages, model)
#     st.sidebar.caption(f"🧮 Tokens in buffer: {used_tokens} / {max_tokens}")


# lab3.py — Lab 3c: Refined Chatbot with "More Info" Loop (Fixed)
import os
import re
import streamlit as st
from openai import OpenAI
import tiktoken

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

def count_tokens(messages, model="gpt-4o-mini") -> int:
    try:
        enc = tiktoken.encoding_for_model(model)
    except Exception:
        enc = tiktoken.get_encoding("cl100k_base")
    total = 0
    for msg in messages:
        total += len(enc.encode(msg["content"]))
    return total

def truncate_messages(messages, model, max_tokens: int):
    truncated = []
    total = 0
    for msg in reversed(messages):
        tokens = count_tokens([msg], model)
        if total + tokens <= max_tokens:
            truncated.insert(0, msg)
            total += tokens
        else:
            break
    return truncated

YES_PAT = re.compile(r"^(y|yes|yeah|yep|sure|ok|okay|more)$", re.I)
NO_PAT  = re.compile(r"^(n|no|nope|nah)$", re.I)

def classify_followup(text: str) -> str:
    """Return one of: 'yes', 'no', 'expand', 'new_question'."""
    t = text.strip()
    if YES_PAT.match(t):
        return "yes"
    if NO_PAT.match(t):
        return "no"
    # Heuristic: question words → new question
    lower = t.lower()
    if t.endswith("?") or lower.startswith(
        ("what", "how", "why", "when", "where", "who", "explain", "define", "tell")
    ):
        return "new_question"
    return "expand"  # e.g. "give pseudocode"

# ========================= App Config =========================
st.set_page_config(page_title="Lab 3c — Refined Chatbot", layout="centered")
st.title("Lab 3c — Refined Chatbot (Token Buffer + More Info Loop)")

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

    max_tokens = st.slider("Max tokens to keep in buffer", 500, 4000, 2000, step=100)
    st.caption("Chat history will be truncated so total input ≤ this value.")

    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.session_state.mode = "question"
        st.session_state.last_topic = ""
        st.rerun()

# ========================= Initialize State =========================
if "messages" not in st.session_state:
    st.session_state.messages = []
if "mode" not in st.session_state:
    st.session_state.mode = "question"
if "last_topic" not in st.session_state:
    st.session_state.last_topic = ""

# ========================= Render Chat History =========================
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ========================= Handle Input =========================
if prompt := st.chat_input("Type here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    def send_reply(system_instruction: str):
        buffer = truncate_messages(st.session_state.messages, model, max_tokens)
        messages = [{"role": "system", "content": system_instruction}] + buffer

        with st.chat_message("assistant"):
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

        st.session_state.messages.append({"role": "assistant", "content": reply})
        return reply

    # ========================= Controller =========================
    if st.session_state.mode == "question":
        # New Q → answer + ask followup
        st.session_state.last_topic = prompt
        send_reply("Explain answers simply so a 10-year-old can understand.")
        followup = "Do you want more info?"
        with st.chat_message("assistant"):
            st.markdown(followup)
        st.session_state.messages.append({"role": "assistant", "content": followup})
        st.session_state.mode = "followup"

    else:  # mode == "followup"
        action = classify_followup(prompt)

        if action == "yes":
            send_reply(
                f"Provide more detail, examples, and analogies about '{st.session_state.last_topic}', "
                "but keep it simple so a 10-year-old can understand."
            )
            followup = "Do you want more info?"
            with st.chat_message("assistant"):
                st.markdown(followup)
            st.session_state.messages.append({"role": "assistant", "content": followup})

        elif action == "no":
            reply = "Okay! What question can I help you with next?"
            with st.chat_message("assistant"):
                st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
            st.session_state.mode = "question"

        elif action == "new_question":
            st.session_state.last_topic = prompt
            send_reply("Explain answers simply so a 10-year-old can understand.")
            followup = "Do you want more info?"
            with st.chat_message("assistant"):
                st.markdown(followup)
            st.session_state.messages.append({"role": "assistant", "content": followup})
            st.session_state.mode = "followup"

        else:  # expand
            send_reply(
                f"Expand the previous answer about '{st.session_state.last_topic}' focusing on '{prompt}'. "
                "Keep it simple so a 10-year-old can understand."
            )
            followup = "Do you want more info?"
            with st.chat_message("assistant"):
                st.markdown(followup)
            st.session_state.messages.append({"role": "assistant", "content": followup})

    # ========================= Token usage =========================
    used_tokens = count_tokens(st.session_state.messages, model)
    st.sidebar.caption(f"🧮 Tokens in buffer: {used_tokens} / {max_tokens}")
