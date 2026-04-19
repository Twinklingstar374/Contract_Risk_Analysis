import streamlit as st
from pypdf import PdfReader
from agent.graph import build_agent

# ---------------- CONFIG ----------------
st.set_page_config(page_title="ContractRisk AI", layout="wide")

# ---------------- CSS ----------------
st.markdown("""
<style>
body { background-color: #0E1117; color: white; }

.risk-card { 
    background-color: #161B22; 
    border-radius: 12px; 
    padding: 16px; 
    border: 1px solid #30363D; 
    margin-bottom: 12px;
}

.badge {
    padding: 4px 10px;
    border-radius: 10px;
    font-size: 12px;
    float: right;
    color: white;
}

.high { background: #F85149; }
.medium { background: #F59E0B; }
.low { background: #10B981; }
</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.header("📂 Upload Contract")
    file = st.file_uploader("Upload PDF", type="pdf")

    if file:
        reader = PdfReader(file)
        text = "\n".join([p.extract_text() for p in reader.pages])

        st.success("PDF Loaded")

        if st.button("🚀 Run Analysis", use_container_width=True):
            agent = build_agent()
            result = agent.invoke({"text": text})
            st.session_state["data"] = result

# ---------------- MAIN ----------------
if "data" in st.session_state:

    res = st.session_state["data"]
    clauses = res["results"]

    col1, col2 = st.columns([1.2, 2])

    # LEFT: DOCUMENT
    with col1:
        st.subheader("📄 Document")
        st.text_area("Preview", res["text"][:5000], height=600)

    # RIGHT: ANALYSIS
    with col2:
        st.subheader("📊 Clause Analysis")

        for item in clauses:

            txt = item["analysis"].lower()

            if "high" in txt:
                color = "high"
                label = "High Risk"
            elif "medium" in txt:
                color = "medium"
                label = "Medium Risk"
            else:
                color = "low"
                label = "Low Risk"

            st.markdown(f"""
            <div class="risk-card">
                <span class="badge {color}">{label}</span>

                <b>Clause:</b><br>
                <div style="color:#9ca3af;">
                    {item['clause']}
                </div>

                <br><b>Analysis:</b><br>
                {item['analysis']}
            </div>
            """, unsafe_allow_html=True)

        st.download_button(
            "📄 Download Report",
            res["report"],
            file_name="report.txt"
        )

else:
    st.info("Upload a contract and click Run Analysis")