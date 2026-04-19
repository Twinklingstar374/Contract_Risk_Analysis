import streamlit as st
import plotly.graph_objects as go
from pypdf import PdfReader
from agent.graph import build_agent
from rag.llm_rag import client

# ================================================================
# CONFIG
# ================================================================
st.set_page_config(page_title="ContractRisk AI", layout="wide", page_icon="⚖️")

# ================================================================
# GLOBAL CSS — Premium Dark Theme + Animations
# ================================================================
st.markdown("""
<style>
/* ---------- RESET & BASE ---------- */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
* { font-family: 'Inter', sans-serif; }
[data-testid="stSidebar"] { display: none !important; }
header[data-testid="stHeader"] { background: transparent !important; }
.block-container { padding-top: 1rem !important; }
section[data-testid="stMain"] { background: #0a0a0f; }

/* ---------- ANIMATED HERO BACKGROUND ---------- */
.hero-bg-wrapper {
    position: relative;
    min-height: 88vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    text-align: center;
    padding: 2rem;
    background: radial-gradient(ellipse at 20% 50%, rgba(99,102,241,0.08) 0%, transparent 50%),
                radial-gradient(ellipse at 80% 20%, rgba(192,132,252,0.06) 0%, transparent 50%),
                radial-gradient(ellipse at 60% 80%, rgba(244,114,182,0.05) 0%, transparent 50%);
}

/* Animated Mesh Grid */
.hero-bg-wrapper::before {
    content: '';
    position: absolute;
    inset: 0;
    background-image:
        linear-gradient(rgba(99,102,241,0.06) 1px, transparent 1px),
        linear-gradient(90deg, rgba(99,102,241,0.06) 1px, transparent 1px);
    background-size: 60px 60px;
    animation: gridShift 20s linear infinite;
    z-index: 0;
}
@keyframes gridShift {
    0%   { transform: translate(0, 0); }
    100% { transform: translate(60px, 60px); }
}

/* Floating Orbs */
.orb {
    position: absolute;
    border-radius: 50%;
    filter: blur(80px);
    z-index: 0;
    pointer-events: none;
}
.orb-1 {
    width: 400px; height: 400px;
    background: radial-gradient(circle, rgba(99,102,241,0.3), transparent 70%);
    top: 5%; left: -5%;
    animation: float1 14s ease-in-out infinite alternate;
}
.orb-2 {
    width: 350px; height: 350px;
    background: radial-gradient(circle, rgba(192,132,252,0.25), transparent 70%);
    bottom: 0%; right: -3%;
    animation: float2 18s ease-in-out infinite alternate;
}
.orb-3 {
    width: 280px; height: 280px;
    background: radial-gradient(circle, rgba(244,114,182,0.2), transparent 70%);
    top: 50%; left: 35%;
    animation: float3 12s ease-in-out infinite alternate;
}
.orb-4 {
    width: 200px; height: 200px;
    background: radial-gradient(circle, rgba(16,185,129,0.15), transparent 70%);
    top: 15%; right: 15%;
    animation: float1 16s ease-in-out infinite alternate-reverse;
}
@keyframes float1 {
    0%   { transform: translate(0, 0) scale(1); }
    50%  { transform: translate(30px, -25px) scale(1.1); }
    100% { transform: translate(-15px, 20px) scale(0.95); }
}
@keyframes float2 {
    0%   { transform: translate(0, 0) scale(1); }
    50%  { transform: translate(-25px, 15px) scale(1.08); }
    100% { transform: translate(20px, -30px) scale(0.97); }
}
@keyframes float3 {
    0%   { transform: translate(0, 0) scale(1); }
    50%  { transform: translate(20px, 20px) scale(1.05); }
    100% { transform: translate(-10px, -15px) scale(1); }
}

/* Particles */
.particle {
    position: absolute;
    border-radius: 50%;
    z-index: 0;
    pointer-events: none;
    opacity: 0;
    animation: particleFloat linear infinite;
}
.p1 { width:3px;height:3px;background:rgba(165,180,252,0.7);top:85%;left:10%;animation-duration:18s;animation-delay:0s; }
.p2 { width:4px;height:4px;background:rgba(192,132,252,0.6);top:90%;left:80%;animation-duration:22s;animation-delay:-4s; }
.p3 { width:2px;height:2px;background:rgba(165,180,252,0.5);top:88%;left:45%;animation-duration:16s;animation-delay:-2s; }
.p4 { width:3px;height:3px;background:rgba(244,114,182,0.5);top:92%;left:25%;animation-duration:20s;animation-delay:-6s; }
.p5 { width:4px;height:4px;background:rgba(99,102,241,0.6);top:87%;left:65%;animation-duration:24s;animation-delay:-8s; }
.p6 { width:2px;height:2px;background:rgba(52,211,153,0.5);top:95%;left:55%;animation-duration:15s;animation-delay:-3s; }
.p7 { width:3px;height:3px;background:rgba(165,180,252,0.4);top:82%;left:90%;animation-duration:19s;animation-delay:-10s; }
.p8 { width:2px;height:2px;background:rgba(192,132,252,0.5);top:93%;left:35%;animation-duration:21s;animation-delay:-7s; }

@keyframes particleFloat {
    0%   { transform: translateY(0); opacity: 0; }
    10%  { opacity: 0.8; }
    90%  { opacity: 0.6; }
    100% { transform: translateY(-85vh); opacity: 0; }
}

/* Hero Content */
.hero-content {
    position: relative;
    z-index: 1;
}
.hero-badge {
    background: rgba(99, 102, 241, 0.15);
    border: 1px solid rgba(99,102,241,0.4);
    color: #a5b4fc;
    padding: 6px 18px;
    border-radius: 999px;
    font-size: 13px;
    letter-spacing: 1px;
    text-transform: uppercase;
    font-weight: 600;
    margin-bottom: 1.5rem;
    display: inline-block;
    animation: fadeUp 0.8s ease-out;
}
.hero-title {
    font-size: 4.2rem;
    font-weight: 900;
    line-height: 1.08;
    margin-bottom: 1rem;
    background: linear-gradient(135deg, #818cf8, #c084fc, #f472b6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: fadeUp 1s ease-out 0.15s both;
}
.hero-sub {
    font-size: 1.15rem;
    color: #9ca3af;
    max-width: 580px;
    margin: 0 auto 2rem;
    line-height: 1.7;
    animation: fadeUp 1s ease-out 0.3s both;
}
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(28px); }
    to   { opacity: 1; transform: translateY(0); }
}

/* Feature Pills */
.feature-row {
    display: flex; gap: 10px; justify-content: center; flex-wrap: wrap;
    margin-bottom: 2.5rem;
    animation: fadeUp 1s ease-out 0.45s both;
}
.feature-pill {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 12px;
    padding: 10px 18px;
    color: #d1d5db;
    font-size: 13px;
    font-weight: 500;
    transition: all 0.3s;
}
.feature-pill:hover {
    background: rgba(99,102,241,0.12);
    border-color: rgba(99,102,241,0.4);
    color: #a5b4fc;
    transform: translateY(-2px);
}

/* ---------- UPLOAD AREA ---------- */
.upload-zone {
    background: rgba(255,255,255,0.03);
    border: 2px dashed rgba(99,102,241,0.35);
    border-radius: 16px;
    padding: 2.5rem;
    max-width: 700px;
    width: 100%;
    margin: 0 auto;
    transition: border-color 0.3s;
}
.upload-zone:hover { border-color: rgba(99,102,241,0.7); }

/* ---------- DASHBOARD TABS ---------- */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 14px;
    padding: 5px;
    gap: 4px;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 10px;
    padding: 10px 22px;
    font-weight: 600;
    font-size: 14px;
    color: #9ca3af;
    background: transparent;
    border: none;
    transition: all 0.3s;
}
.stTabs [data-baseweb="tab"]:hover {
    color: #e5e7eb;
    background: rgba(255,255,255,0.05);
}
.stTabs [aria-selected="true"] {
    background: rgba(99,102,241,0.15) !important;
    color: #a5b4fc !important;
}
.stTabs [data-baseweb="tab-highlight"],
.stTabs [data-baseweb="tab-border"] {
    display: none;
}

/* ---------- METRIC CARDS ---------- */
.metric-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 1.4rem 1rem;
    text-align: center;
    transition: transform 0.2s, border-color 0.3s;
}
.metric-card:hover {
    transform: translateY(-4px);
    border-color: rgba(99,102,241,0.5);
}
.metric-value {
    font-size: 2rem;
    font-weight: 800;
    margin-bottom: 0.2rem;
}
.metric-label {
    font-size: 0.8rem;
    color: #9ca3af;
    text-transform: uppercase;
    letter-spacing: 1px;
}

/* ---------- RISK CARDS ---------- */
.risk-card {
    border-radius: 14px;
    padding: 20px;
    margin-bottom: 16px;
    color: #fff;
    transition: transform 0.2s;
}
.risk-card:hover { transform: translateY(-2px); }
.high-card { background: linear-gradient(135deg, rgba(248,81,73,0.12), rgba(248,81,73,0.04)); border: 1px solid rgba(248,81,73,0.4); }
.medium-card { background: linear-gradient(135deg, rgba(251,191,36,0.12), rgba(251,191,36,0.04)); border: 1px solid rgba(251,191,36,0.4); }
.low-card { background: linear-gradient(135deg, rgba(52,211,153,0.12), rgba(52,211,153,0.04)); border: 1px solid rgba(52,211,153,0.4); }

.pill {
    display: inline-block; padding: 4px 14px; border-radius: 999px;
    font-size: 12px; font-weight: 700; color: #fff; letter-spacing: 0.5px;
}
.pill-high { background: #ef4444; }
.pill-med  { background: #f59e0b; }
.pill-low  { background: #10b981; }

.clause-text {
    background: rgba(0,0,0,0.3);
    padding: 12px;
    border-radius: 10px;
    margin: 10px 0;
    color: #d1d5db;
    font-size: 13px;
    line-height: 1.7;
    border-left: 3px solid rgba(255,255,255,0.1);
}
.analysis-text { color: #e5e7eb; font-size: 13px; line-height: 1.6; margin: 6px 0; }
.rec-text { color: #93c5fd; font-size: 13px; line-height: 1.6; margin: 6px 0; }

/* ---------- REC CARDS ---------- */
.rec-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 14px;
    padding: 18px;
    margin-bottom: 14px;
    transition: all 0.3s;
}
.rec-card:hover {
    border-color: rgba(99,102,241,0.4);
    transform: translateY(-2px);
    background: rgba(255,255,255,0.05);
}
.rec-card-header {
    display: flex; align-items: center; justify-content: space-between;
    margin-bottom: 10px;
}
.rec-clause-num {
    color: #9ca3af; font-size: 13px; font-weight: 600;
    text-transform: uppercase; letter-spacing: 0.5px;
}
.rec-action {
    background: rgba(99,102,241,0.1);
    border: 1px solid rgba(99,102,241,0.25);
    border-radius: 8px;
    padding: 12px;
    margin-top: 8px;
    color: #c7d2fe;
    font-size: 13px;
    line-height: 1.6;
}

/* ---------- SUMMARY TABLE ---------- */
.summary-table {
    width: 100%; border-collapse: separate; border-spacing: 0;
    background: rgba(255,255,255,0.02);
    border-radius: 14px; overflow: hidden;
    border: 1px solid rgba(255,255,255,0.08);
}
.summary-table th {
    background: rgba(99,102,241,0.1);
    color: #a5b4fc; font-weight: 600; font-size: 12px;
    padding: 12px 14px; text-align: left;
    text-transform: uppercase; letter-spacing: 0.5px;
}
.summary-table td {
    padding: 12px 14px; color: #d1d5db; font-size: 13px;
    border-top: 1px solid rgba(255,255,255,0.05);
    line-height: 1.5;
}
.summary-table tr:hover td {
    background: rgba(255,255,255,0.03);
}

.chat-msg {
    display: flex; gap: 10px; margin-bottom: 12px; align-items: flex-start;
}
.chat-avatar {
    width: 32px; height: 32px; border-radius: 8px; display: flex;
    align-items: center; justify-content: center; font-size: 14px; flex-shrink: 0;
}
.avatar-user { background: linear-gradient(135deg, #6366f1, #8b5cf6); }
.avatar-ai   { background: linear-gradient(135deg, #10b981, #34d399); }
.chat-bubble {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 10px;
    padding: 12px 14px;
    color: #e5e7eb;
    font-size: 13px;
    line-height: 1.6;
    max-width: 88%;
}

/* ---------- SECTION HEADERS ---------- */
.section-head {
    font-size: 1.4rem; font-weight: 700; color: #f3f4f6;
    margin-bottom: 0.2rem;
}
.section-sub {
    font-size: 0.85rem; color: #6b7280; margin-bottom: 1.2rem;
}
.dash-title {
    font-size: 1.8rem; font-weight: 800;
    background: linear-gradient(135deg, #818cf8, #c084fc);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    margin: 0;
}

/* ---------- CHART CARD ---------- */
.chart-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 1rem;
    margin-bottom: 1rem;
}
.chart-title {
    color: #f3f4f6; font-weight: 600; font-size: 14px; margin-bottom: 4px;
}

/* ---------- DISCLAIMER ---------- */
.disclaimer {
    text-align: center; color: #6b7280; font-size: 12px;
    padding: 2rem 1rem 1rem;
    border-top: 1px solid rgba(255,255,255,0.06);
    margin-top: 2rem;
}

/* Hide streamlit branding */
#MainMenu, footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ================================================================
# HELPERS
# ================================================================
def classify_risk(analysis_text):
    txt = analysis_text.lower()
    if "high" in txt:
        return "High"
    elif "medium" in txt:
        return "Medium"
    return "Low"


def generate_recommendation(clause, analysis):
    prompt = (
        f"Given this legal clause:\n{clause}\n\n"
        f"And its analysis:\n{analysis}\n\n"
        "Provide a very short, actionable 'Suggested Fix' or 'Recommendation' "
        "(1-2 sentences max). Return only the recommendation text."
    )
    try:
        resp = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )
        return resp.choices[0].message.content.strip()
    except Exception:
        return "Unable to generate recommendation at this time."


def ask_contract_question(question, clauses):
    context = "\n\n".join(
        [f"Clause: {c['clause']}\nAnalysis: {c['analysis']}" for c in clauses]
    )
    prompt = (
        "You are a helpful legal AI assistant. Based on the following analyzed "
        "contract clauses, answer the user's question clearly and concisely.\n\n"
        f"{context}\n\nQuestion: {question}\nAnswer:"
    )
    try:
        resp = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        return f"Sorry, I couldn't process that question. Error: {str(e)}"


# ================================================================
# CHARTS
# ================================================================
def build_risk_pie(high, medium, low):
    colors = ["#ef4444", "#f59e0b", "#10b981"]
    fig = go.Figure(go.Pie(
        labels=["High Risk", "Medium Risk", "Low Risk"],
        values=[high, medium, low],
        hole=0.55,
        marker=dict(colors=colors, line=dict(color="#0a0a0f", width=3)),
        textinfo="label+value",
        textfont=dict(size=13, color="#e5e7eb"),
        hoverinfo="label+percent+value",
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e5e7eb"),
        showlegend=False,
        margin=dict(t=20, b=20, l=20, r=20),
        height=280,
        annotations=[dict(
            text=f"<b>{high+medium+low}</b><br><span style='font-size:11px;color:#9ca3af'>clauses</span>",
            x=0.5, y=0.5, font_size=22, font_color="#f3f4f6",
            showarrow=False,
        )],
    )
    return fig


def build_risk_bar(high, medium, low):
    fig = go.Figure()
    categories = ["High", "Medium", "Low"]
    values = [high, medium, low]
    colors = ["#ef4444", "#f59e0b", "#10b981"]
    for cat, val, col in zip(categories, values, colors):
        fig.add_trace(go.Bar(
            x=[cat], y=[val], name=cat,
            marker=dict(color=col, cornerradius=6),
            text=[val], textposition="outside",
            textfont=dict(size=14, color="#e5e7eb"),
            hovertemplate=f"{cat}: {val}<extra></extra>",
        ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e5e7eb"),
        showlegend=False,
        xaxis=dict(showgrid=False, color="#9ca3af"),
        yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.06)", color="#9ca3af", dtick=1),
        margin=dict(t=30, b=40, l=40, r=20),
        height=280,
        bargap=0.5,
    )
    return fig


# ================================================================
# PAGE: LANDING / HERO
# ================================================================
def render_landing_page():
    # Animated hero with pure CSS — no base64 images
    st.markdown("""
    <div class="hero-bg-wrapper">
        <div class="orb orb-1"></div>
        <div class="orb orb-2"></div>
        <div class="orb orb-3"></div>
        <div class="orb orb-4"></div>
        <div class="particle p1"></div>
        <div class="particle p2"></div>
        <div class="particle p3"></div>
        <div class="particle p4"></div>
        <div class="particle p5"></div>
        <div class="particle p6"></div>
        <div class="particle p7"></div>
        <div class="particle p8"></div>
        <div class="hero-content">
            <div class="hero-badge">⚡ Powered by RAG + LangGraph Agents</div>
            <div class="hero-title">AI Contract<br>Risk Analyzer</div>
            <p class="hero-sub">
                Upload any legal contract and get instant AI-powered risk analysis,
                clause-by-clause breakdown, and actionable recommendations.
            </p>
            <div class="feature-row">
                <div class="feature-pill">🔍 Clause Extraction</div>
                <div class="feature-pill">⚠️ Risk Classification</div>
                <div class="feature-pill">💡 AI Recommendations</div>
                <div class="feature-pill">🤖 Contract Chatbot</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- Centered upload ---
    _, center, _ = st.columns([1.2, 2, 1.2])
    with center:
        tab_pdf, tab_text = st.tabs(["📄  Upload PDF", "✏️  Paste Text"])

        with tab_pdf:
            uploaded_file = st.file_uploader(
                "Drop your contract PDF here",
                type="pdf",
                label_visibility="collapsed",
                key="pdf_upload",
            )
            if uploaded_file:
                st.success(f"✅ **{uploaded_file.name}** loaded — {uploaded_file.size // 1024} KB")

        with tab_text:
            pasted_text = st.text_area(
                "Paste contract text below",
                height=220,
                placeholder="Paste your contract clauses here…",
                key="text_paste",
            )

        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

        if st.button("🚀  Analyze Contract", use_container_width=True, type="primary"):
            contract_text = None

            if uploaded_file:
                reader = PdfReader(uploaded_file)
                contract_text = "\n".join(
                    [p.extract_text() for p in reader.pages if p.extract_text()]
                )
            elif pasted_text and len(pasted_text.strip()) > 50:
                contract_text = pasted_text.strip()

            if not contract_text:
                st.error("Please upload a PDF or paste contract text (min 50 characters).")
                return

            with st.spinner("🔍 Extracting clauses and analyzing risks…"):
                agent = build_agent()
                result = agent.invoke({"text": contract_text})

            with st.spinner("💡 Generating actionable recommendations…"):
                for r in result.get("results", []):
                    r["recommendation"] = generate_recommendation(r["clause"], r["analysis"])
                    r["risk_level"] = classify_risk(r["analysis"])

            st.session_state["data"] = result
            st.session_state["page"] = "results"
            st.rerun()

    st.markdown(
        '<div class="disclaimer">⚠️ This is AI-generated analysis and not legal advice. '
        "Always consult a qualified attorney for legal matters.</div>",
        unsafe_allow_html=True,
    )


# ================================================================
# PAGE: RESULTS DASHBOARD
# ================================================================
def render_results_page():
    res = st.session_state["data"]
    clauses = res.get("results", [])

    for c in clauses:
        if "risk_level" not in c:
            c["risk_level"] = classify_risk(c["analysis"])

    high = sum(1 for c in clauses if c["risk_level"] == "High")
    medium = sum(1 for c in clauses if c["risk_level"] == "Medium")
    low = sum(1 for c in clauses if c["risk_level"] == "Low")
    total = len(clauses)
    overall = "High" if high > 0 else ("Medium" if medium > 0 else "Low")
    overall_color = {"High": "#ef4444", "Medium": "#f59e0b", "Low": "#10b981"}[overall]
    risk_score = max(0, min(100, int(((high * 3 + medium * 1.5) / (total * 3)) * 100))) if total > 0 else 0
    gauge_color = "#ef4444" if risk_score >= 60 else ("#f59e0b" if risk_score >= 30 else "#10b981")

    # ------ Header ------
    top_l, top_r = st.columns([3, 1])
    with top_l:
        st.markdown(
            '<p class="dash-title">📊 Analysis Dashboard</p>'
            '<p class="section-sub" style="margin:0;">AI-powered clause-by-clause risk breakdown</p>',
            unsafe_allow_html=True,
        )
    with top_r:
        if st.button("← New Analysis", use_container_width=True):
            for key in ["data", "page", "chat_history"]:
                st.session_state.pop(key, None)
            st.rerun()

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # ------ Metric cards ------
    c1, c2, c3, c4, c5 = st.columns(5)
    metrics = [
        (c1, str(total), "Total Clauses", "#818cf8"),
        (c2, overall, "Overall Risk", overall_color),
        (c3, str(high), "High Risk", "#ef4444"),
        (c4, str(medium), "Medium Risk", "#f59e0b"),
        (c5, str(low), "Low Risk", "#10b981"),
    ]
    for col, val, label, color in metrics:
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value" style="color:{color};">{val}</div>
                <div class="metric-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

    # ====================================
    # TABS
    # ====================================
    tab_overview, tab_clauses, tab_recs, tab_chat = st.tabs([
        "📈  Analytics",
        "🔍  Clause Analysis",
        "💡  Recommendations",
        "🤖  AI Chatbot",
    ])

    # ──────────────────────────────────────
    # TAB 1: Analytics Overview
    # ──────────────────────────────────────
    with tab_overview:
        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

        col_gauge, col_summary = st.columns(2, gap="medium")

        with col_gauge:
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            st.markdown('<p class="chart-title">⚡ Overall Risk Score</p>', unsafe_allow_html=True)
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=risk_score,
                number=dict(suffix="%", font=dict(size=40, color="#f3f4f6")),
                gauge=dict(
                    axis=dict(range=[0, 100], tickcolor="#6b7280", tickfont=dict(color="#6b7280")),
                    bar=dict(color=gauge_color, thickness=0.75),
                    bgcolor="rgba(255,255,255,0.04)",
                    borderwidth=0,
                    steps=[
                        dict(range=[0, 30], color="rgba(16,185,129,0.08)"),
                        dict(range=[30, 60], color="rgba(245,158,11,0.08)"),
                        dict(range=[60, 100], color="rgba(239,68,68,0.08)"),
                    ],
                    threshold=dict(line=dict(color="#f3f4f6", width=2), thickness=0.8, value=risk_score),
                ),
            ))
            fig_gauge.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#e5e7eb"),
                margin=dict(t=40, b=10, l=30, r=30), height=260,
            )
            st.plotly_chart(fig_gauge, use_container_width=True, config={"displayModeBar": False})
            st.markdown('</div>', unsafe_allow_html=True)

        with col_summary:
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            st.markdown('<p class="chart-title">📋 Quick Summary</p>', unsafe_allow_html=True)
            st.markdown(f"""
            <table class="summary-table">
                <thead><tr><th>Metric</th><th>Value</th><th>Status</th></tr></thead>
                <tbody>
                    <tr><td>Total Clauses Analyzed</td><td><b>{total}</b></td><td>✅ Complete</td></tr>
                    <tr><td>High Risk Clauses</td><td><b style="color:#ef4444;">{high}</b></td>
                        <td>{"🔴 Action Required" if high > 0 else "✅ Clear"}</td></tr>
                    <tr><td>Medium Risk Clauses</td><td><b style="color:#f59e0b;">{medium}</b></td>
                        <td>{"🟡 Review Suggested" if medium > 0 else "✅ Clear"}</td></tr>
                    <tr><td>Low Risk Clauses</td><td><b style="color:#10b981;">{low}</b></td>
                        <td>🟢 Acceptable</td></tr>
                    <tr><td>Overall Risk Score</td><td><b style="color:{gauge_color};">{risk_score}%</b></td>
                        <td>{"🔴 High" if risk_score >= 60 else ("🟡 Medium" if risk_score >= 30 else "🟢 Low")}</td></tr>
                </tbody>
            </table>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

        chart_l, chart_r = st.columns(2, gap="medium")
        with chart_l:
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            st.markdown('<p class="chart-title">🍩 Risk Distribution</p>', unsafe_allow_html=True)
            st.plotly_chart(build_risk_pie(high, medium, low), use_container_width=True, config={"displayModeBar": False})
            st.markdown('</div>', unsafe_allow_html=True)
        with chart_r:
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            st.markdown('<p class="chart-title">📊 Risk Count Breakdown</p>', unsafe_allow_html=True)
            st.plotly_chart(build_risk_bar(high, medium, low), use_container_width=True, config={"displayModeBar": False})
            st.markdown('</div>', unsafe_allow_html=True)

    # ──────────────────────────────────────
    # TAB 2: Clause Analysis
    # ──────────────────────────────────────
    with tab_clauses:
        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
        st.markdown(
            '<p class="section-head">🔍 Clause-by-Clause Breakdown</p>'
            '<p class="section-sub">Every clause analyzed with risk level, analysis, and recommendation</p>',
            unsafe_allow_html=True,
        )

        filter_choice = st.radio(
            "Filter by risk level:",
            ["All", "High Risk", "Medium Risk", "Low Risk"],
            horizontal=True,
            label_visibility="collapsed",
        )

        filtered = clauses
        if filter_choice == "High Risk":
            filtered = [c for c in clauses if c["risk_level"] == "High"]
        elif filter_choice == "Medium Risk":
            filtered = [c for c in clauses if c["risk_level"] == "Medium"]
        elif filter_choice == "Low Risk":
            filtered = [c for c in clauses if c["risk_level"] == "Low"]

        if not filtered:
            st.info(f"No {filter_choice.lower()} clauses found.")
        else:
            col_a, col_b = st.columns(2, gap="medium")
            for i, item in enumerate(filtered):
                level = item["risk_level"]
                card_cls = {"High": "high-card", "Medium": "medium-card", "Low": "low-card"}[level]
                pill_cls = {"High": "pill-high", "Medium": "pill-med", "Low": "pill-low"}[level]
                clause_idx = clauses.index(item) + 1

                with (col_a if i % 2 == 0 else col_b):
                    st.markdown(f"""
                    <div class="risk-card {card_cls}">
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                            <span style="color:#9ca3af; font-size:13px; font-weight:600;">CLAUSE {clause_idx}</span>
                            <span class="pill {pill_cls}">{level} Risk</span>
                        </div>
                        <div class="clause-text">{item['clause']}</div>
                        <div class="analysis-text"><b style="color:#f3f4f6;">🔍 Analysis:</b> {item['analysis']}</div>
                        <div class="rec-text"><b>💡 Recommendation:</b> {item.get('recommendation', 'N/A')}</div>
                    </div>
                    """, unsafe_allow_html=True)

        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

        report = "CONTRACT RISK ANALYSIS REPORT\n" + "=" * 60 + "\n\n"
        report += f"Total Clauses: {total}  |  High: {high}  |  Medium: {medium}  |  Low: {low}\n"
        report += f"Overall Risk: {overall}  |  Risk Score: {risk_score}%\n" + "=" * 60 + "\n\n"
        for i, r in enumerate(clauses):
            report += f"[{i+1}] {r['risk_level']} RISK\n" + "-" * 40 + "\n"
            report += f"Clause: {r['clause']}\n\nAnalysis: {r['analysis']}\n\n"
            report += f"Recommendation: {r.get('recommendation', '')}\n\n"

        st.download_button(
            "⬇️  Download Full Report",
            report,
            file_name="contract_risk_report.txt",
            use_container_width=True,
        )

    # ──────────────────────────────────────
    # TAB 3: Recommendations
    # ──────────────────────────────────────
    with tab_recs:
        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
        st.markdown(
            '<p class="section-head">💡 AI-Powered Recommendations</p>'
            '<p class="section-sub">Actionable suggestions prioritized by risk severity</p>',
            unsafe_allow_html=True,
        )

        sorted_clauses = sorted(
            [(i, c) for i, c in enumerate(clauses)],
            key=lambda x: {"High": 0, "Medium": 1, "Low": 2}.get(x[1]["risk_level"], 3),
        )

        groups = [
            ([x for x in sorted_clauses if x[1]["risk_level"] == "High"],
             "🔴 High Priority — Immediate Action Required", "#ef4444", "pill-high", "High Risk"),
            ([x for x in sorted_clauses if x[1]["risk_level"] == "Medium"],
             "🟡 Medium Priority — Review Suggested", "#f59e0b", "pill-med", "Medium Risk"),
            ([x for x in sorted_clauses if x[1]["risk_level"] == "Low"],
             "🟢 Low Priority — Acceptable", "#10b981", "pill-low", "Low Risk"),
        ]

        for group_items, title, color, pill_cls, pill_text in groups:
            if group_items:
                st.markdown(
                    f'<p style="color:{color}; font-weight:700; font-size:15px; '
                    f'margin:20px 0 10px;">{title}</p>',
                    unsafe_allow_html=True,
                )
                for idx, item in group_items:
                    clause_preview = item['clause'][:180] + ('...' if len(item['clause']) > 180 else '')
                    st.markdown(f"""
                    <div class="rec-card" style="border-left: 3px solid {color};">
                        <div class="rec-card-header">
                            <span class="rec-clause-num">Clause {idx+1}</span>
                            <span class="pill {pill_cls}">{pill_text}</span>
                        </div>
                        <div style="color:#d1d5db; font-size:13px; line-height:1.5; margin-bottom:6px;">
                            {clause_preview}
                        </div>
                        <div class="rec-action">
                            💡 <b>Recommendation:</b> {item.get('recommendation', 'N/A')}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

    # ──────────────────────────────────────
    # TAB 4: AI Chatbot
    # ──────────────────────────────────────
    with tab_chat:
        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

        st.markdown(
            '<p class="section-head">🤖 Ask About Your Contract</p>'
            '<p class="section-sub">Chat with AI about the analyzed clauses, risks, or recommendations</p>',
            unsafe_allow_html=True,
        )

        # Initialize chat history
        if "chat_history" not in st.session_state:
            st.session_state["chat_history"] = []

        # Chat container
        st.markdown("""
        <div class="chat-container">
            <div class="chat-header">
                <div class="chat-dot"></div>
                <span style="color:#f3f4f6; font-weight:600; font-size:14px;">AI Contract Assistant</span>
                <span style="color:#6b7280; font-size:11px; margin-left:auto;">Powered by LLM</span>
            </div>
        """, unsafe_allow_html=True)

        if not st.session_state["chat_history"]:
            st.markdown("""
            <div class="chat-msg">
                <div class="chat-avatar avatar-ai">🤖</div>
                <div class="chat-bubble">
                    Hi! I've analyzed your contract. Ask me anything about the clauses,
                    risks, or recommendations.<br><br>
                    • <i>What are the high-risk clauses?</i><br>
                    • <i>Is there a termination penalty?</i><br>
                    • <i>Summarize the key risks.</i><br>
                    • <i>What should I negotiate first?</i>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            for msg in st.session_state["chat_history"]:
                if msg["role"] == "user":
                    st.markdown(f"""
                    <div class="chat-msg" style="justify-content:flex-end;">
                        <div class="chat-bubble" style="background:rgba(99,102,241,0.12); border-color:rgba(99,102,241,0.25);">
                            {msg['content']}
                        </div>
                        <div class="chat-avatar avatar-user">👤</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="chat-msg">
                        <div class="chat-avatar avatar-ai">🤖</div>
                        <div class="chat-bubble">{msg['content']}</div>
                    </div>
                    """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        # Input area
        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
        input_col, btn_col = st.columns([5, 1])
        with input_col:
            user_question = st.text_input(
                "Ask a question…",
                placeholder="e.g. What are the most risky clauses? What should I negotiate?",
                label_visibility="collapsed",
                key="chat_input",
            )
        with btn_col:
            send_pressed = st.button("Send ➤", use_container_width=True, type="primary")

        if user_question and send_pressed:
            st.session_state["chat_history"].append({"role": "user", "content": user_question})
            with st.spinner("Thinking…"):
                answer = ask_contract_question(user_question, clauses)
            st.session_state["chat_history"].append({"role": "assistant", "content": answer})
            st.rerun()

        if st.session_state["chat_history"]:
            if st.button("🗑️ Clear Chat", use_container_width=True):
                st.session_state["chat_history"] = []
                st.rerun()

    # Footer
    st.markdown(
        '<div class="disclaimer">⚠️ This is AI-generated analysis and not legal advice. '
        "Always consult a qualified attorney for legal matters.</div>",
        unsafe_allow_html=True,
    )


# ================================================================
# ROUTER
# ================================================================
if st.session_state.get("page") == "results" and "data" in st.session_state:
    render_results_page()
else:
    render_landing_page()