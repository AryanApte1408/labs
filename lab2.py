import os
import time
import hashlib
import streamlit as st
import fitz  # PyMuPDF
from openai import OpenAI

# ========================= Helpers =========================
def _get_openai_api_key() -> str | None:
    # 1) Streamlit Cloud secrets
    try:
        key = st.secrets["OPENAI_API_KEY"]
        if key:
            return key
    except Exception:
        pass
    # 2) Local .env fallback (optional)
    try:
        from dotenv import load_dotenv  # type: ignore
        load_dotenv()
    except Exception:
        pass
    return os.getenv("OPENAI_API_KEY")

def read_pdf(file) -> str:
    """Extract text from PDF using PyMuPDF."""
    file.seek(0)
    data = file.read()
    text = []
    with fitz.open(stream=data, filetype="pdf") as doc:
        for page in doc:
            text.append(page.get_text() or "")
    return "\n".join(text)

def normalize(val: float, vmin: float, vmax: float, invert: bool = False) -> float:
    """Map val to [0,1] given [vmin,vmax]; optionally invert for 'lower is better'."""
    if vmax == vmin:
        return 1.0
    x = (val - vmin) / (vmax - vmin)
    return 1 - x if invert else x

def file_sha1(path: str) -> str:
    try:
        with open(path, "rb") as f:
            return hashlib.sha1(f.read()).hexdigest()[:12]
    except Exception:
        return "unknown"

def style_instruction(choice: str) -> str:
    if choice == "100 words":
        return "Summarize the document in about 100 words."
    if choice == "2 connecting paragraphs":
        return "Summarize the document in two connected paragraphs with smooth transitions."
    return "Summarize the document in exactly five concise bullet points."

# ========================= App Header =========================
st.set_page_config(page_title="Lab 2 — Weighted PDF Summarizer", layout="centered")
st.title("Lab 2 — Weighted PDF Summarizer (Model Comparison)")

running_path = os.path.abspath(__file__) if "__file__" in globals() else "(interactive)"
st.caption(f"Running file: `{running_path}` | sha1: `{file_sha1(running_path)}`")

st.write(
    "Upload a PDF and generate a summary with two different models. "
    "We score each result by a weighted combination of Quality, Speed, and Cost."
)

# ========================= Sidebar =========================
with st.sidebar:
    st.header("Settings")

    # Summary options required by the lab
    language = st.selectbox(
        "Summary language",
        ["English", "Spanish", "French", "German", "Hindi", "Chinese", "Arabic"],
        index=0,
    )
    summary_type = st.selectbox(
        "Summary type",
        ["100 words", "2 connecting paragraphs", "5 bullet points"],
        index=0,
    )

    # Weights
    st.subheader("Weights")
    w_quality = st.slider("Quality weight", 0.0, 1.0, 0.50, 0.05)
    w_speed   = st.slider("Speed weight",   0.0, 1.0, 0.30, 0.05)
    w_cost    = st.slider("Cost weight",    0.0, 1.0, 0.20, 0.05)
    s = w_quality + w_speed + w_cost
    if s == 0:
        w_quality, w_speed, w_cost = 0.5, 0.3, 0.2
    else:
        w_quality, w_speed, w_cost = (w_quality/s, w_speed/s, w_cost/s)
    st.caption(f"Normalized: quality={w_quality:.2f}, speed={w_speed:.2f}, cost={w_cost:.2f}")

# ========================= API Client =========================
api_key = _get_openai_api_key()
if not api_key:
    st.error(
        "OPENAI_API_KEY not found. Add it to Streamlit Secrets as `OPENAI_API_KEY`, "
        "or set it in a local `.env` file."
    )
    st.stop()

client = OpenAI(api_key=api_key)

# ========================= Upload =========================
uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])
if not uploaded_file:
    st.stop()

# Read PDF once and cache in session
if "pdf_text" not in st.session_state:
    st.session_state.pdf_text = read_pdf(uploaded_file)

doc_text = st.session_state.pdf_text
if not doc_text.strip():
    st.warning("No extractable text found in this PDF.")
    st.stop()

# ========================= Models & Pricing =========================
# Compare 4o-mini (default) vs 4o (advanced) per lab spec
models = ["gpt-4o-mini", "gpt-4o"]

# Update these numbers to match your current pricing per 1M tokens (USD)
# They are placeholders; keep the structure for scoring.
pricing = {
    "gpt-4o-mini": {"in": 0.15, "out": 0.60},   # $/1M tokens (placeholder)
    "gpt-4o":      {"in": 2.50, "out": 10.00},  # $/1M tokens (placeholder)
}

# ========================= Run both models =========================
prompt_user = (
    f"{style_instruction(summary_type)}\n"
    f"Write the summary in {language}.\n\n"
    f"Document Text:\n{doc_text}"
)

results = {}
tabs = st.tabs(models)

for i, m in enumerate(models):
    with tabs[i]:
        st.subheader(m)
        with st.spinner(f"Generating with {m}..."):
            t0 = time.perf_counter()
            resp = client.chat.completions.create(
                model=m,
                messages=[
                    {"role": "system", "content": "You are a careful assistant. Answer only based on the provided text."},
                    {"role": "user", "content": prompt_user},
                ],
                # not streaming so we can capture usage and latency
            )
            latency = time.perf_counter() - t0

        content = resp.choices[0].message.content
        usage = getattr(resp, "usage", None)
        in_tok = getattr(usage, "prompt_tokens", None) or getattr(usage, "input_tokens", None)
        out_tok = getattr(usage, "completion_tokens", None) or getattr(usage, "output_tokens", None)

        # Cost estimate (best-effort; adjust pricing values above)
        cost = 0.0
        if in_tok is not None and out_tok is not None and m in pricing:
            cost = (in_tok / 1_000_000) * pricing[m]["in"] + (out_tok / 1_000_000) * pricing[m]["out"]

        st.markdown(content)
        st.caption(
            f"Latency: {latency:.2f}s • "
            f"In/Out tokens: {in_tok if in_tok is not None else '—'}/"
            f"{out_tok if out_tok is not None else '—'} • "
            f"Estimated cost: ${cost:.4f}"
        )

        results[m] = {
            "answer": content,
            "latency": latency,
            "tokens_in": in_tok or 0,
            "tokens_out": out_tok or 0,
            "cost": cost,
        }

# ========================= Scoring =========================
# Basic quality proxy: longer answers often carry more detail; clip to a range
# Replace with a rubric or a human score if you want stricter evaluation.
def crude_quality(answer: str) -> float:
    n = len(answer.split())
    return max(0.0, min(1.0, n / 250.0))  # 0..1 around ~250 words

latencies = [results[m]["latency"] for m in models]
costs     = [results[m]["cost"]    for m in models]
qualities = [crude_quality(results[m]["answer"]) for m in models]

for m in models:
    r = results[m]
    r["score_quality"] = crude_quality(r["answer"])                      # higher better
    r["score_speed"]   = normalize(r["latency"], min(latencies), max(latencies), invert=True)  # lower better
    r["score_cost"]    = normalize(r["cost"],     min(costs),     max(costs),     invert=True) # lower better
    r["composite"]     = (
        r["score_quality"] * w_quality +
        r["score_speed"]   * w_speed   +
        r["score_cost"]    * w_cost
    )
    r["contrib_quality"] = r["score_quality"] * w_quality
    r["contrib_speed"]   = r["score_speed"]   * w_speed
    r["contrib_cost"]    = r["score_cost"]    * w_cost

# ========================= Table & Summary =========================
st.header("Weighted Criteria & Ranking")
table_rows = []
for m in models:
    r = results[m]
    table_rows.append({
        "Model": m,
        "Quality (0–1)": f"{r['score_quality']:.2f}",
        "Speed (0–1)":   f"{r['score_speed']:.2f}",
        "Cost (0–1)":    f"{r['score_cost']:.2f}",
        "Composite":     f"{r['composite']:.2f}",
    })
st.table(table_rows)

best = max(models, key=lambda m: results[m]["composite"])
ranked = sorted(models, key=lambda m: results[m]["composite"], reverse=True)
best_r = results[best]

contribs = {
    "quality": best_r["contrib_quality"],
    "speed":   best_r["contrib_speed"],
    "cost":    best_r["contrib_cost"],
}
main_driver = max(contribs, key=contribs.get)

best_quality = max(models, key=lambda m: results[m]["score_quality"])
best_speed   = max(models, key=lambda m: results[m]["score_speed"])
best_cost    = max(models, key=lambda m: results[m]["score_cost"])

st.success(f"Best Overall (by your weights): {best}")

summary = []
summary.append(
    f"With your weights (quality {w_quality:.0%}, speed {w_speed:.0%}, cost {w_cost:.0%}), "
    f"{best} ranks first with a composite score of {best_r['composite']:.2f}."
)
summary.append(
    f"The largest contribution to the winning score is {main_driver} "
    f"({best_r[f'contrib_{main_driver}']:.2f} of the total)."
)

is_compromise = (best != best_quality) and (best != best_speed) and (best != best_cost)
if is_compromise:
    summary.append(
        f"{best} is not the top model on any single criterion "
        f"(best quality: {best_quality}, best speed: {best_speed}, best cost: {best_cost}), "
        "but it offers the strongest overall balance given your weights."
    )

if len(ranked) > 1:
    runner = ranked[1]
    diff = results[best]["composite"] - results[runner]["composite"]
    summary.append(
        f"The runner-up is {runner} with a composite of {results[runner]['composite']:.2f}, "
        f"{diff:.2f} points behind."
    )

st.subheader("Summary")
st.write(" ".join(summary))
st.caption("Adjust the weights to see how the ranking and rationale change.")
