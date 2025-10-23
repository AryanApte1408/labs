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
    Fact-checks a claim using OpenAI gpt-5 with structured JSON output.
    Returns: dictionary containing verdict, explanation, confidence, sources, timestamp.
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
        # System prompt
        system_prompt = """You are an expert fact-checker and research assistant. Your job is to:

1. Analyze the given claim carefully and identify key assertions.
2. Research the claim using your reasoning and current knowledge.
3. Evaluate evidence from multiple perspectives.
4. Provide a verdict: TRUE, FALSE, PARTIALLY TRUE, or UNVERIFIED.
5. Explain reasoning with evidence.
6. Provide credible sources supporting your analysis.

Respond ONLY in valid JSON:
{
    "claim": "the original claim verbatim",
    "verdict": "TRUE/FALSE/PARTIALLY TRUE/UNVERIFIED",
    "confidence": "HIGH/MEDIUM/LOW",
    "explanation": "Detailed reasoning and evidence.",
    "sources": [
        {"title": "Source title", "url": "https://example.com", "snippet": "Relevant quote or summary"}
    ],
    "last_updated": "YYYY-MM-DD HH:MM:SS"
}

Verdict guidelines:
- TRUE: Strong, consistent evidence supports claim.
- FALSE: Clear evidence refutes claim.
- PARTIALLY TRUE: Mix of true and false elements.
- UNVERIFIED: Not enough reliable evidence.

Source priority:
- Peer-reviewed journals (.edu)
- Government agencies (.gov)
- Trusted orgs (.org: WHO, CDC, Mayo Clinic)
- Fact-checking orgs (Snopes, PolitiFact)
"""

        # ✅ Fixed: Use max_completion_tokens instead of max_tokens
        response = client.chat.completions.create(
            model="gpt-5",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Fact-check this claim: {claim}"}
            ],
            response_format={"type": "json_object"},
            temperature=0.3,
            max_completion_tokens=2000
        )

        # Parse JSON
        result_text = response.choices[0].message.content
        result = json.loads(result_text)

        # Ensure timestamp
        if "last_updated" not in result:
            result["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Ensure all keys
        required_fields = ["claim", "verdict", "confidence", "explanation", "sources"]
        for field in required_fields:
            if field not in result:
                result[field] = "N/A" if field != "sources" else []

        return result

    except json.JSONDecodeError as e:
        return {
            "claim": claim,
            "verdict": "ERROR",
            "confidence": "N/A",
            "explanation": f"Failed to parse response as JSON: {e}",
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
    """Format sources for display"""
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
    st.error("⚠️ Missing OPENAI_API_KEY. Please add it in `.streamlit/secrets.toml` or as env variable.")
    st.stop()
client = OpenAI(api_key=openai_api_key)

# ================================================================
# Sidebar UI
# ================================================================
with st.sidebar:
    st.header("ℹ️ About")
    st.info("""
    This tool uses **gpt-5** to:
    - Analyze factual claims  
    - Provide verdicts with confidence  
    - Generate credible citations  
    - Build transparency through sources  
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
    st.caption("💡 Note: gpt-5 provides enhanced reasoning and structured output.")

# ================================================================
# Session State
# ================================================================
if "claim_history" not in st.session_state:
    st.session_state.claim_history = []
if "user_claim" not in st.session_state:
    st.session_state.user_claim = ""

# ================================================================
# Main Input Area
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
        "TRUE": {"icon": "🟢", "color": "#28a745"},
        "FALSE": {"icon": "🔴", "color": "#dc3545"},
        "PARTIALLY TRUE": {"icon": "🟡", "color": "#ffc107"},
        "UNVERIFIED": {"icon": "⚪", "color": "#6c757d"},
        "ERROR": {"icon": "⚫", "color": "#343a40"}
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
        st.warning("⚠️ No sources were provided for this claim.")

    with st.expander("ℹ️ Additional Information"):
        st.write(f"**Timestamp:** {result.get('last_updated','N/A')}")
        st.write("**Model:** gpt-5")
        st.write("**Mode:** Structured JSON Output")

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
# Reflection Section
# ================================================================
st.divider()
with st.expander("💭 Lab 6 Reflection & Discussion"):
    st.markdown("""
    ### 🤔 Reflection
    **1. How did the model’s reasoning differ from chat models?**
    - gpt-5 provided structured, verifiable JSON results.
    - Each verdict had explicit confidence levels.
    - Explanations cited sources directly.

    **2. Were the sources credible and diverse?**
    - Focused on .gov, .edu, and .org domains.
    - Represented peer-reviewed and factual outlets.

    **3. How does this enhance trust?**
    - Transparent evidence chain.
    - Reproducible, structured outputs.
    - Easy to audit and export.
    """)

# ================================================================
# Footer
# ================================================================
st.divider()
st.caption("Built with Streamlit + OpenAI gpt-5 • Lab 6: AI Fact-Checker + Citation Builder")
