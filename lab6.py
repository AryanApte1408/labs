# ================================================================
# Lab 6 — AI Fact-Checker + Citation Builder
# Built with Streamlit + OpenAI gpt-5
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
    """
    Fact-check a claim using OpenAI gpt-5 with structured JSON output.
    """
    if not client:
        return {
            "claim": claim,
            "verdict": "ERROR",
            "confidence": "N/A",
            "explanation": "OpenAI client not initialized. Please check your API key.",
            "sources": [],
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

    try:
        # ------------------------------------------------------------
        # System Prompt
        # ------------------------------------------------------------
        system_prompt = """You are an expert fact-checker and research assistant.
Your task is to:
1. Analyze the user's claim.
2. Evaluate evidence from multiple perspectives.
3. Provide a verdict (TRUE, FALSE, PARTIALLY TRUE, or UNVERIFIED).
4. Explain reasoning clearly.
5. Include 3–5 credible sources with short snippets.

Respond ONLY in this exact JSON format:
{
  "claim": "the claim verbatim",
  "verdict": "TRUE/FALSE/PARTIALLY TRUE/UNVERIFIED",
  "confidence": "HIGH/MEDIUM/LOW",
  "explanation": "Detailed reasoning, context, and evidence.",
  "sources": [
    {"title": "Source title", "url": "https://example.com", "snippet": "Relevant quote"}
  ],
  "last_updated": "YYYY-MM-DD HH:MM:SS"
}

Guidelines:
- Use peer-reviewed, .gov, .edu, .org, and fact-checking sites.
- Verdict rules:
  - TRUE: Supported by strong evidence
  - FALSE: Contradicted by evidence
  - PARTIALLY TRUE: Contains mixed accuracy
  - UNVERIFIED: Insufficient evidence
"""

        # ------------------------------------------------------------
        # OpenAI Call (fixed)
        # ------------------------------------------------------------
        response = client.chat.completions.create(
            model="gpt-5",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Fact-check this claim: {claim}"}
            ],
            response_format={"type": "json_object"},
            max_completion_tokens=2000  # ✅ correct param
        )

        result_text = response.choices[0].message.content
        result = json.loads(result_text)

        if "last_updated" not in result:
            result["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        required_fields = ["claim", "verdict", "confidence", "explanation", "sources"]
        for f in required_fields:
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
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    except Exception as e:
        return {
            "claim": claim,
            "verdict": "ERROR",
            "confidence": "N/A",
            "explanation": f"Error during fact-checking: {e}",
            "sources": [],
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }


def format_sources_as_markdown(sources: list) -> str:
    """Format sources for display in markdown."""
    if not sources:
        return "*No sources available*"
    out = ""
    for i, s in enumerate(sources, 1):
        title = s.get("title", "Untitled Source")
        url = s.get("url", "#")
        snippet = s.get("snippet", "")
        out += f"{i}. **[{title}]({url})**\n"
        if snippet:
            out += f"   > *{snippet}*\n\n"
    return out


# ================================================================
# Streamlit Configuration
# ================================================================
st.set_page_config(page_title="Lab 6 — AI Fact-Checker", page_icon="🔍", layout="centered")
st.title("🔍 Lab 6 — AI Fact-Checker + Citation Builder")
st.markdown("*Verify claims with gpt-5 powered research and evidence-based citations*")

# ================================================================
# API Key Initialization
# ================================================================
openai_api_key = _get_openai_api_key()
if not openai_api_key:
    st.error("⚠️ Missing OPENAI_API_KEY. Add it in `.streamlit/secrets.toml` or as an env variable.")
    st.stop()
client = OpenAI(api_key=openai_api_key)

# ================================================================
# Sidebar
# ================================================================
with st.sidebar:
    st.header("ℹ️ About")
    st.info("""
    This tool uses **gpt-5** to:
    - Analyze factual claims  
    - Provide evidence-based verdicts  
    - Generate credible citations  
    - Increase transparency and trust  
    """)
    st.divider()

    st.header("📝 Sample Claims")
    examples = [
        "Is dark chocolate healthy?",
        "Can drinking coffee prevent cancer?",
        "Is Pluto still classified as a planet?",
        "Does vitamin C cure the common cold?",
        "Are electric cars better for the environment?"
    ]
    for ex in examples:
        if st.button(ex, key=ex, use_container_width=True):
            st.session_state.user_claim = ex

    st.divider()
    st.caption("💡 Note: gpt-5 provides structured, reasoning-based outputs.")

# ================================================================
# Session State
# ================================================================
if "claim_history" not in st.session_state:
    st.session_state.claim_history = []
if "user_claim" not in st.session_state:
    st.session_state.user_claim = ""

# ================================================================
# Input
# ================================================================
user_claim = st.text_input(
    "**Enter a factual claim to verify:**",
    value=st.session_state.user_claim,
    placeholder="e.g., Is dark chocolate healthy?",
    key="claim_input"
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
    with st.spinner("🔎 Verifying claim with gpt-5..."):
        result = fact_check_claim(user_claim, client)
        st.session_state.claim_history.insert(0, result)
        st.session_state.claim_history = st.session_state.claim_history[:10]
        st.session_state.user_claim = ""

    # ============================================================
    # Display Results
    # ============================================================
    st.divider()
    verdict = result.get("verdict", "UNKNOWN")
    confidence = result.get("confidence", "N/A")

    verdict_map = {
        "TRUE": {"icon": "🟢"},
        "FALSE": {"icon": "🔴"},
        "PARTIALLY TRUE": {"icon": "🟡"},
        "UNVERIFIED": {"icon": "⚪"},
        "ERROR": {"icon": "⚫"}
    }
    cfg = verdict_map.get(verdict, {"icon": "⚪"})

    c1, c2, c3 = st.columns(3)
    c1.metric("📊 Verdict", f"{cfg['icon']} {verdict}")
    c2.metric("🎯 Confidence", confidence)
    c3.metric("📚 Sources", len(result.get("sources", [])))

    st.subheader("🔖 Claim")
    st.info(result.get("claim", user_claim))

    st.subheader("📝 Analysis & Explanation")
    st.write(result.get("explanation", "No explanation provided."))

    st.subheader("📚 Sources & Citations")
    srcs = result.get("sources", [])
    if srcs:
        st.markdown(format_sources_as_markdown(srcs))
    else:
        st.warning("⚠️ No sources provided for this claim.")

    with st.expander("ℹ️ Additional Information"):
        st.write(f"**Timestamp:** {result.get('last_updated','N/A')}")
        st.write("**Model:** gpt-5")
        st.write("**Mode:** Structured JSON Output")

    with st.expander("🔧 View Raw JSON Response"):
        st.json(result)

elif run_check:
    st.warning("⚠️ Please enter a valid claim before checking.")

# ================================================================
# History
# ================================================================
if st.session_state.claim_history:
    st.divider()
    st.subheader("📜 Recent Fact-Checks")
    for i, item in enumerate(st.session_state.claim_history, 1):
        verdict = item.get("verdict", "UNKNOWN")
        claim_text = item.get("claim", "")
        preview = claim_text[:80] + ("..." if len(claim_text) > 80 else "")
        icon = verdict_map.get(verdict, {"icon": "⚪"})["icon"]

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
    - gpt-5 uses structured JSON instead of conversational output.
    - Clear verdicts, evidence, and confidence levels.

    **2. Credibility & Diversity**
    - Prioritizes .gov, .edu, and .org domains.
    - Encourages evidence triangulation from multiple perspectives.

    **3. Trust & Transparency**
    - Every result includes reasoning and sources.
    - Easy to audit and replicate fact-checks.
    """)

# ================================================================
# Footer
# ================================================================
st.divider()
st.caption("Built with Streamlit + OpenAI gpt-5 • Lab 6: AI Fact-Checker + Citation Builder")
