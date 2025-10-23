# ================================================================
# Lab 6 — AI Fact-Checker + Citation Builder
# Built with Streamlit + OpenAI gpt-4.1 (Responses API)
# ================================================================
import os
import streamlit as st
from openai import OpenAI
import json
from datetime import datetime
from typing import Dict, Any

# ================================================================
# Helper Functions
# ================================================================
def _get_openai_api_key() -> str | None:
    """Get OpenAI API key from Streamlit secrets or environment"""
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


def fact_check_claim(claim: str, client: OpenAI) -> Dict[str, Any]:
    """Fact-check a claim using OpenAI gpt-4.1 via Responses API."""
    if not client:
        return {
            "claim": claim,
            "verdict": "ERROR",
            "confidence": "N/A",
            "explanation": "OpenAI client not initialized. Please check your API key.",
            "sources": [],
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

    try:
        # ------------------------------------------------------------
        # System Prompt
        # ------------------------------------------------------------
        system_prompt = """You are an expert fact-checker and research assistant.
Your task:
1. Evaluate the truthfulness of the given claim.
2. Use reasoning and evidence from reliable sources.
3. Return ONLY a valid JSON object in the format below.

{
  "claim": "original claim",
  "verdict": "TRUE/FALSE/PARTIALLY TRUE/UNVERIFIED",
  "confidence": "HIGH/MEDIUM/LOW",
  "explanation": "Detailed reasoning and evidence.",
  "sources": [
    {"title": "Source title", "url": "https://example.com", "snippet": "Relevant quote"}
  ],
  "last_updated": "YYYY-MM-DD HH:MM:SS"
}

Guidelines:
- TRUE: Strong supporting evidence
- FALSE: Strong contradicting evidence
- PARTIALLY TRUE: Mixed accuracy
- UNVERIFIED: Insufficient or inconclusive data
Prefer .gov, .edu, .org, or peer-reviewed sources."""

        # ------------------------------------------------------------
        # OpenAI Responses API call (using gpt-4.1)
        # ------------------------------------------------------------
        response = client.responses.create(
            model="gpt-4.1",  # ✅ Using GPT-4.1
            input=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Fact-check this claim: {claim}"},
            ],
            response_format={"type": "json_object"},
            max_output_tokens=2000,
        )

        # Parse model JSON output
        result_text = response.output[0].content[0].text.strip()
        result = json.loads(result_text)

        if "last_updated" not in result:
            result["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        required = ["claim", "verdict", "confidence", "explanation", "sources"]
        for f in required:
            if f not in result:
                result[f] = "N/A" if f != "sources" else []

        return result

    except json.JSONDecodeError as e:
        return {
            "claim": claim,
            "verdict": "ERROR",
            "confidence": "N/A",
            "explanation": f"Failed to parse JSON: {e}",
            "sources": [],
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
    except Exception as e:
        return {
            "claim": claim,
            "verdict": "ERROR",
            "confidence": "N/A",
            "explanation": f"Error during fact-checking: {e}",
            "sources": [],
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }


def format_sources_as_markdown(sources: list) -> str:
    """Format sources for display in markdown."""
    if not sources:
        return "*No sources available*"
    md = ""
    for i, s in enumerate(sources, 1):
        title = s.get("title", "Untitled Source")
        url = s.get("url", "#")
        snippet = s.get("snippet", "")
        md += f"{i}. **[{title}]({url})**\n"
        if snippet:
            md += f"   > *{snippet}*\n\n"
    return md


# ================================================================
# Streamlit Configuration
# ================================================================
st.set_page_config(page_title="Lab 6 — AI Fact-Checker", page_icon="🔍", layout="centered")
st.title("🔍 Lab 6 — AI Fact-Checker + Citation Builder")
st.markdown("*Verify claims with GPT-4.1 powered research and evidence-based citations*")

# ================================================================
# API Key Initialization
# ================================================================
openai_api_key = _get_openai_api_key()
if not openai_api_key:
    st.error("⚠️ Missing OPENAI_API_KEY. Add it in `.streamlit/secrets.toml` or as an environment variable.")
    st.stop()
client = OpenAI(api_key=openai_api_key)

# ================================================================
# Sidebar
# ================================================================
with st.sidebar:
    st.header("ℹ️ About")
    st.info("""
    This tool uses **GPT-4.1** (Responses API) to:
    - Analyze factual claims  
    - Provide verdicts with confidence  
    - Generate credible citations  
    - Build transparency and trust  
    """)
    st.divider()

    st.header("📝 Sample Claims")
    examples = [
        "Is dark chocolate healthy?",
        "Can drinking coffee prevent cancer?",
        "Is Pluto still classified as a planet?",
        "Does vitamin C cure the common cold?",
        "Are electric cars better for the environment?",
    ]
    for ex in examples:
        if st.button(ex, key=ex, use_container_width=True):
            st.session_state.user_claim = ex

    st.divider()
    st.caption("💡 Note: GPT-4.1 provides structured, reasoning-based outputs.")

# ================================================================
# Session State
# ================================================================
if "claim_history" not in st.session_state:
    st.session_state.claim_history = []
if "user_claim" not in st.session_state:
    st.session_state.user_claim = ""

# ================================================================
# Main Input
# ================================================================
user_claim = st.text_input(
    "**Enter a factual claim to verify:**",
    value=st.session_state.user_claim,
    placeholder="e.g., Is dark chocolate healthy?",
    key="claim_input",
)

col1, col2 = st.columns([2, 1])
with col1:
    run_check = st.button("🔍 Check Fact", type="primary", use_container_width=True)
with col2:
    if st.button("🗑️ Clear History", use_container_width=True):
        st.session_state.claim_history = []
        st.rerun()

# ================================================================
# Fact-Check Execution
# ================================================================
if run_check and user_claim.strip():
    with st.spinner("🔎 Verifying claim with GPT-4.1..."):
        result = fact_check_claim(user_claim, client)
        st.session_state.claim_history.insert(0, result)
        st.session_state.claim_history = st.session_state.claim_history[:10]
        st.session_state.user_claim = ""

    # Display Results
    st.divider()
    verdict = result.get("verdict", "UNKNOWN")
    confidence = result.get("confidence", "N/A")

    verdict_icons = {
        "TRUE": "🟢",
        "FALSE": "🔴",
        "PARTIALLY TRUE": "🟡",
        "UNVERIFIED": "⚪",
        "ERROR": "⚫",
    }
    icon = verdict_icons.get(verdict, "⚪")

    c1, c2, c3 = st.columns(3)
    c1.metric("📊 Verdict", f"{icon} {verdict}")
    c2.metric("🎯 Confidence", confidence)
    c3.metric("📚 Sources", len(result.get("sources", [])))

    st.subheader("🔖 Claim")
    st.info(result.get("claim", user_claim))

    st.subheader("📝 Analysis & Explanation")
    st.write(result.get("explanation", "No explanation provided."))

    st.subheader("📚 Sources & Citations")
    sources = result.get("sources", [])
    if sources:
        st.markdown(format_sources_as_markdown(sources))
    else:
        st.warning("⚠️ No sources provided for this claim.")

    with st.expander("ℹ️ Additional Information"):
        st.write(f"**Timestamp:** {result.get('last_updated', 'N/A')}")
        st.write("**Model:** GPT-4.1")
        st.write("**Mode:** Structured JSON Output (Responses API)")

    with st.expander("🔧 View Raw JSON Response"):
        st.json(result)

elif run_check:
    st.warning("⚠️ Please enter a valid claim before checking.")

# ================================================================
# Claim History
# ================================================================
if st.session_state.claim_history:
    st.divider()
    st.subheader("📜 Recent Fact-Checks")
    for i, item in enumerate(st.session_state.claim_history, 1):
        verdict = item.get("verdict", "UNKNOWN")
        claim_text = item.get("claim", "")
        preview = claim_text[:80] + ("..." if len(claim_text) > 80 else "")
        icon = verdict_icons.get(verdict, "⚪")
        with st.expander(f"#{i} | {icon} {verdict} — {preview}"):
            st.write(f"**🎯 Verdict:** {verdict}")
            st.write(f"**📊 Confidence:** {item.get('confidence','N/A')}")
            st.write(f"**📝 Explanation:** {item.get('explanation','N/A')}")
            srcs = item.get("sources", [])
            if srcs:
                st.markdown(format_sources_as_markdown(srcs))
            else:
                st.write("*No sources available*")

# ================================================================
# Reflection
# ================================================================
st.divider()
with st.expander("💭 Lab 6 Reflection & Discussion"):
    st.markdown("""
    ### 🤔 Reflection
    **1. Model Reasoning vs. Chat Models**
    - GPT-4.1 uses structured JSON output instead of conversational text.
    - Each verdict includes confidence and evidence.

    **2. Credibility & Diversity**
    - Prioritizes .gov, .edu, and .org domains.
    - Promotes multiple independent sources.

    **3. Trust & Transparency**
    - Every result is evidence-backed and timestamped.
    - Easy to verify, audit, and reproduce.
    """)

# ================================================================
# Footer
# ================================================================
st.divider()
st.caption("Built with Streamlit + OpenAI GPT-4.1 • Lab 6: AI Fact-Checker + Citation Builder")
