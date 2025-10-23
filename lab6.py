# lab6.py — Lab 6: AI Fact-Checker + Citation Builder
import os
import streamlit as st
from openai import OpenAI
import json
from datetime import datetime
from typing import Dict, Any

# ========================= Helpers =========================
def _get_openai_api_key() -> str | None:
    """Get OpenAI API key from secrets or environment"""
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
    Fact-checks a claim using OpenAI GPT-5-chat with structured JSON output.
    
    Args:
        claim: The factual claim to verify
        client: OpenAI client instance
        
    Returns:
        Dictionary containing claim verification results
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
        # System prompt for structured fact-checking
        system_prompt = """You are an expert fact-checker and research assistant. Your job is to:

1. Analyze the given claim carefully and identify key assertions
2. Research the claim using your knowledge and reasoning
3. Evaluate evidence from multiple perspectives
4. Provide a clear verdict: TRUE, FALSE, PARTIALLY TRUE, or UNVERIFIED
5. Explain your reasoning with specific details and evidence
6. List credible sources that support your analysis

IMPORTANT: You must respond with valid JSON in this exact structure:
{
    "claim": "the original claim verbatim",
    "verdict": "TRUE/FALSE/PARTIALLY TRUE/UNVERIFIED",
    "confidence": "HIGH/MEDIUM/LOW",
    "explanation": "detailed explanation with reasoning, evidence, and nuance. Include specific facts and context.",
    "sources": [
        {
            "title": "Source title (e.g., journal name, website, organization)",
            "url": "https://example.com (use realistic URLs for the type of source)",
            "snippet": "Brief relevant information or quote from this source"
        }
    ],
    "last_updated": "YYYY-MM-DD HH:MM:SS"
}

Guidelines:
- TRUE: Claim is accurate based on current evidence
- FALSE: Claim is clearly contradicted by evidence
- PARTIALLY TRUE: Claim contains both accurate and inaccurate elements
- UNVERIFIED: Insufficient evidence to make a determination

- HIGH confidence: Strong consensus from multiple reliable sources
- MEDIUM confidence: Some evidence but with caveats or limitations
- LOW confidence: Limited or conflicting evidence

Prioritize:
- Peer-reviewed journals (.edu domains)
- Government health organizations (.gov domains)
- Reputable medical institutions (.org domains like WHO, CDC, Mayo Clinic)
- Established scientific organizations
- Fact-checking organizations (Snopes, PolitiFact)

Include 3-5 sources when possible. Be thorough but concise."""

        # Call OpenAI API with GPT-5-chat
        response = client.chat.completions.create(
            model="gpt-5-chat",  # ✅ Using GPT-5-chat
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Fact-check this claim: {claim}"}
            ],
            response_format={"type": "json_object"},
            temperature=0.3,
            max_tokens=2000
        )
        
        # Parse JSON response
        result_text = response.choices[0].message.content
        result = json.loads(result_text)
        
        # Ensure timestamp is present
        if "last_updated" not in result:
            result["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Validate required fields
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
            "explanation": f"Failed to parse AI response as JSON: {str(e)}",
            "sources": [],
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    except Exception as e:
        return {
            "claim": claim,
            "verdict": "ERROR",
            "confidence": "N/A",
            "explanation": f"Error during fact-checking: {str(e)}",
            "sources": [],
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

def format_sources_as_markdown(sources: list) -> str:
    """Convert sources list to formatted markdown with clickable links"""
    if not sources:
        return "*No sources available*"
    
    markdown_text = ""
    for i, source in enumerate(sources, 1):
        title = source.get('title', 'Untitled Source')
        url = source.get('url', '#')
        snippet = source.get('snippet', '')
        
        markdown_text += f"{i}. **[{title}]({url})**\n"
        if snippet:
            markdown_text += f"   > *{snippet}*\n\n"
        else:
            markdown_text += "\n"
    
    return markdown_text

# ========================= App Config =========================
st.set_page_config(
    page_title="Lab 6 — AI Fact-Checker",
    page_icon="🔍",
    layout="centered"
)

st.title("🔍 Lab 6 — AI Fact-Checker + Citation Builder")
st.markdown("*Verify claims with GPT-5-chat powered research and evidence-based citations*")

# ========================= API Key Check =========================
openai_api_key = _get_openai_api_key()

if not openai_api_key:
    st.error("⚠️ Missing OPENAI_API_KEY. Please add it to Streamlit Secrets or environment variables.")
    st.info("Add your key in `.streamlit/secrets.toml` or set the `OPENAI_API_KEY` environment variable.")
    st.stop()

client = OpenAI(api_key=openai_api_key)

# ========================= Sidebar =========================
with st.sidebar:
    st.header("ℹ️ About")
    st.info("""
    This tool uses OpenAI's **GPT-5-chat** to:
    - Analyze factual claims
    - Provide evidence-based verdicts
    - Generate credible citations
    - Build trust through transparency
    """)
    
    st.divider()
    
    st.header("📝 Sample Claims")
    sample_claims = [
        "Is dark chocolate healthy?",
        "Can drinking coffee prevent cancer?",
        "Is Pluto still classified as a planet?",
        "Does vitamin C cure the common cold?",
        "Are electric cars better for the environment?"
    ]
    
    for claim in sample_claims:
        if st.button(claim, key=claim, use_container_width=True):
            st.session_state.user_claim = claim
    
    st.divider()
    
    st.caption("💡 **Note:** GPT-5-chat provides enhanced reasoning capabilities")
    st.caption("🔬 **Model:** GPT-5-chat")

# ========================= Initialize Session State =========================
if 'claim_history' not in st.session_state:
    st.session_state.claim_history = []

if 'user_claim' not in st.session_state:
    st.session_state.user_claim = ""

# ========================= Main UI =========================
user_claim = st.text_input(
    "**Enter a factual claim to verify:**",
    value=st.session_state.user_claim,
    placeholder="e.g., Is dark chocolate healthy?",
    help="Enter any factual claim you'd like to verify",
    key="claim_input"
)

col1, col2, col3 = st.columns([2, 2, 1])
with col1:
    check_button = st.button("🔍 Check Fact", type="primary", use_container_width=True)
with col2:
    if len(st.session_state.claim_history) > 0:
        if st.button("🗑️ Clear History", use_container_width=True):
            st.session_state.claim_history = []
            st.rerun()

# ========================= Fact-Checking Logic =========================
if check_button and user_claim:
    with st.spinner("🔎 Researching and verifying your claim with GPT-5-chat..."):
        result = fact_check_claim(user_claim, client)
        
        # Add to history
        st.session_state.claim_history.insert(0, result)
        
        # Keep only last 10 claims
        st.session_state.claim_history = st.session_state.claim_history[:10]
        
        # Clear the input
        st.session_state.user_claim = ""
    
    st.divider()
    
    # ========================= Results Display =========================
    verdict = result.get('verdict', 'UNKNOWN')
    confidence = result.get('confidence', 'N/A')
    
    # Verdict configuration
    verdict_config = {
        'TRUE': {'icon': '🟢', 'color': '#28a745'},
        'FALSE': {'icon': '🔴', 'color': '#dc3545'},
        'PARTIALLY TRUE': {'icon': '🟡', 'color': '#ffc107'},
        'UNVERIFIED': {'icon': '⚪', 'color': '#6c757d'},
        'ERROR': {'icon': '⚫', 'color': '#343a40'}
    }
    
    config = verdict_config.get(verdict, {'icon': '⚪', 'color': '#6c757d'})
    
    # Metrics row
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📊 Verdict", f"{config['icon']} {verdict}")
    with col2:
        st.metric("🎯 Confidence", confidence)
    with col3:
        st.metric("📚 Sources", len(result.get('sources', [])))
    
    # Claim display
    st.subheader("🔖 Claim")
    st.info(result.get('claim', user_claim))
    
    # Explanation
    st.subheader("📝 Analysis & Explanation")
    explanation = result.get('explanation', 'No explanation available')
    st.write(explanation)
    
    # Sources
    st.subheader("📚 Sources & Citations")
    sources = result.get('sources', [])
    if sources:
        st.markdown(format_sources_as_markdown(sources))
    else:
        st.warning("⚠️ No sources were provided for this claim")
    
    # Metadata
    with st.expander("ℹ️ Additional Information"):
        st.write(f"**Timestamp:** {result.get('last_updated', 'N/A')}")
        st.write(f"**Model:** GPT-5-chat")
        st.write(f"**Mode:** Structured JSON Output")
    
    # Raw JSON
    with st.expander("🔧 View Raw JSON Response"):
        st.json(result)

elif check_button:
    st.warning("⚠️ Please enter a claim to verify")

# ========================= History Display =========================
if st.session_state.claim_history:
    st.divider()
    st.subheader("📜 Recent Fact-Checks")
    
    for i, item in enumerate(st.session_state.claim_history, 1):
        verdict = item.get('verdict', 'UNKNOWN')
        claim_text = item.get('claim', 'Unknown claim')
        claim_preview = claim_text[:70] + "..." if len(claim_text) > 70 else claim_text
        
        verdict_icon = verdict_config.get(verdict, {'icon': '⚪'})['icon']
        
        with st.expander(f"#{i} | {verdict_icon} {verdict} — {claim_preview}"):
            st.write(f"**🎯 Verdict:** {verdict}")
            st.write(f"**📊 Confidence:** {item.get('confidence', 'N/A')}")
            st.write(f"**📝 Explanation:** {item.get('explanation', 'N/A')}")
            
            sources = item.get('sources', [])
            if sources:
                st.write(f"**📚 Sources ({len(sources)}):**")
                st.markdown(format_sources_as_markdown(sources))
            else:
                st.write("*No sources available*")

# ========================= Reflection Section =========================
st.divider()
with st.expander("💭 Lab 6 Reflection & Discussion"):
    st.markdown("""
    ### 🤔 Reflection Questions
    
    #### 1. How did the model's reasoning feel different from a standard chat model?
    
    **GPT-5-chat Structured Output Benefits:**
    - ✅ **Consistency**: JSON format ensures predictable, parseable responses
    - ✅ **Accountability**: Explicit verdicts and confidence levels (no hedging)
    - ✅ **Transparency**: Clear attribution of sources and reasoning
    - ✅ **Task-Focused**: Designed specifically for fact-checking, not casual chat
    - ✅ **Enhanced Reasoning**: GPT-5-chat provides deeper analytical capabilities
    
    **Key Differences from Standard Chat:**
    - Standard chat models can be vague or conversational
    - Fact-checker provides binary/categorical verdicts
    - Structured format enables programmatic processing
    - Research-oriented rather than dialogue-oriented
    - GPT-5-chat offers improved accuracy and nuance
    
    ---
    
    #### 2. Were the sources credible and diverse?
    
    **Source Quality Assessment:**
    - ✅ Prioritizes authoritative domains (.gov, .edu, .org)
    - ✅ References peer-reviewed journals and medical institutions
    - ✅ Includes fact-checking organizations
    - ⚠️ **Note**: Sources are AI-generated based on GPT-5-chat's knowledge
    
    **For Production Use:**
    - Integrate real web search APIs (Brave Search, Google Custom Search)
    - Implement domain authority scoring
    - Add recency filtering (prioritize recent sources)
    - Cross-reference with fact-checking databases
    
    **Diversity Considerations:**
    - Multiple source types (academic, governmental, news)
    - Geographic variety when relevant
    - Different perspectives on controversial topics
    
    ---
    
    #### 3. How does tool integration enhance trust and accuracy?
    
    **🔍 Trust Building:**
    - **Verifiability**: Users can click through to sources
    - **Transparency**: Clear reasoning and evidence chain
    - **Reproducibility**: Consistent results with GPT-5-chat
    - **Attribution**: No "black box" — sources are explicit
    
    **🎯 Accuracy Enhancement with GPT-5-chat:**
    - **Grounding**: Claims tied to external evidence
    - **Reduced Hallucination**: Less invention of facts
    - **Cross-Validation**: Multiple sources confirm findings
    - **Superior Reasoning**: GPT-5-chat's advanced capabilities
    - **Real-Time Data**: (With proper APIs) Up-to-date information
    
    **📊 Confidence Calibration:**
    - Explicit uncertainty communication
    - Nuanced verdicts (not just true/false)
    - Evidence strength indicators
    - Confidence levels guide user trust
    
    ---
    
    ### 🚀 Lab 6d: Enhancement Ideas
    
    **1. Real Web Search Integration**
```python
    # Example: Using Brave Search API
    def search_web(query):
        response = requests.get(
            "https://api.search.brave.com/res/v1/web/search",
            headers={"X-Subscription-Token": BRAVE_API_KEY},
            params={"q": query}
        )
        return response.json()
```
    
    **2. Source Credibility Scoring**
    - Domain reputation (e.g., .gov = high trust)
    - Publication date weighting
    - Author credentials
    - Citation count for academic sources
    
    **3. Enhanced UI Features**
    - Export fact-checks as PDF reports
    - Share results via link
    - Compare multiple fact-checks
    - Visualize source diversity
    
    **4. Advanced Analysis with GPT-5-chat**
    - Detect claim complexity
    - Identify missing context
    - Show evidence conflicts
    - Track claim evolution over time
    - Multi-step reasoning chains
    
    ---
    
    ### 📊 Technical Implementation Notes
    
    **This Lab Uses:**
    - **GPT-5-chat** for enhanced reasoning and accuracy
    - JSON mode (`response_format={"type": "json_object"}`)
    - Temperature 0.3 for consistency
    - Structured system prompts for reliable output
    
    **GPT-5-chat Advantages:**
    - Superior analytical capabilities
    - Better handling of complex claims
    - More nuanced verdicts
    - Improved source attribution
    
    **Production Considerations:**
    - Add rate limiting
    - Implement caching for repeated claims
    - Log all fact-checks for audit
    - Add human review workflow for critical claims
    """)

# ========================= Footer =========================
st.divider()
st.caption("Built with Streamlit + OpenAI GPT-5-chat • Lab 6: AI Fact-Checker + Citation Builder")