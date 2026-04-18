
# import streamlit as st
# import streamlit.components.v1 as components
# import joblib, re, os, json, io
# import nltk
# from nltk.tokenize import word_tokenize
# from nltk.stem import WordNetLemmatizer
# from nltk.corpus import stopwords
# import PyPDF2


# st.markdown("""
# <style>
# #MainMenu,header,footer,
# [data-testid="stHeader"],[data-testid="stToolbar"],
# [data-testid="stDecoration"],[data-testid="stStatusWidget"]{display:none!important;}
# .block-container{padding:0!important;max-width:100%!important;}
# html,body,[data-testid="stAppViewContainer"],[data-testid="stApp"]{background:#06060f!important;}

# /* ── Style native Streamlit widgets to match dark theme ── */
# [data-testid="stTabs"]{background:transparent!important;}
# [data-testid="stTabsTabList"]{
#     background:rgba(255,255,255,.03)!important;
#     border:1px solid rgba(255,255,255,.07)!important;
#     border-radius:10px!important;padding:4px!important;
#     gap:4px!important;
# }
# [data-testid="stTabsTab"]{
#     color:rgba(255,255,255,.38)!important;
#     border-radius:8px!important;
#     font-family:'DM Sans',sans-serif!important;
#     font-size:13px!important;font-weight:500!important;
#     padding:6px 18px!important;
#     border:none!important;background:transparent!important;
# }
# [data-testid="stTabsTab"][aria-selected="true"]{
#     background:rgba(99,102,241,.18)!important;
#     color:#a5b4fc!important;
# }
# [data-testid="stTabsTabPanel"]{padding:0!important;background:transparent!important;}

# textarea{
#     background:rgba(255,255,255,.025)!important;
#     border:1px solid rgba(255,255,255,.08)!important;
#     border-radius:11px!important;color:#dde1f0!important;
#     font-family:'DM Sans',sans-serif!important;
#     font-size:14px!important;line-height:1.75!important;
# }
# textarea:focus{
#     border-color:rgba(99,102,241,.4)!important;
#     box-shadow:0 0 0 3px rgba(99,102,241,.08)!important;
# }
# textarea::placeholder{color:rgba(255,255,255,.16)!important;}

# [data-testid="stFileUploader"]{
#     background:rgba(255,255,255,.02)!important;
#     border:1.5px dashed rgba(255,255,255,.1)!important;
#     border-radius:12px!important;
#     padding:8px!important;
# }
# [data-testid="stFileUploader"]:hover{
#     border-color:rgba(99,102,241,.35)!important;
#     background:rgba(99,102,241,.04)!important;
# }
# [data-testid="stFileUploader"] label{color:rgba(255,255,255,.35)!important;}
# [data-testid="stFileUploaderDropzone"]{background:transparent!important;border:none!important;}
# [data-testid="stFileUploaderDropzoneInstructions"] p,
# [data-testid="stFileUploaderDropzoneInstructions"] span{color:rgba(255,255,255,.35)!important;font-size:13px!important;}

# /* Analyse button */
# [data-testid="stButton"]>button{
#     width:100%!important;height:50px!important;
#     background:linear-gradient(135deg,#5558e3,#c026a8)!important;
#     border:none!important;border-radius:11px!important;
#     color:#fff!important;font-family:'Syne',sans-serif!important;
#     font-size:14px!important;font-weight:700!important;letter-spacing:.4px!important;
#     box-shadow:0 6px 22px rgba(85,88,227,.3)!important;
#     transition:all .2s!important;
# }
# [data-testid="stButton"]>button:hover{
#     transform:translateY(-2px)!important;
#     box-shadow:0 10px 30px rgba(85,88,227,.45)!important;
# }

# /* Section wrapper */
# .analyser-wrap{
#     max-width:800px;margin:0 auto;padding:28px 20px 40px;
# }
# .sec-eyebrow{
#     display:inline-flex;align-items:center;gap:6px;
#     font-size:9.5px;font-weight:600;letter-spacing:1.8px;text-transform:uppercase;
#     color:rgba(165,180,252,.55);margin-bottom:8px;font-family:'DM Sans',sans-serif;
# }
# .sec-title{
#     font-family:'Syne',sans-serif;font-size:26px;font-weight:800;
#     color:#f0f2ff;letter-spacing:-.6px;margin-bottom:3px;line-height:1.15;
# }
# .sec-sub{font-size:13px;color:rgba(220,224,255,.3);margin-bottom:20px;line-height:1.6;font-family:'DM Sans',sans-serif;}
# .ic{
#     background:linear-gradient(160deg,rgba(255,255,255,.03),rgba(255,255,255,.015));
#     border:1px solid rgba(255,255,255,.07);border-radius:16px;padding:22px;
#     box-shadow:0 2px 36px rgba(0,0,0,.3);
# }
# .inp-lbl{
#     font-size:9.5px;font-weight:600;letter-spacing:1.2px;text-transform:uppercase;
#     color:rgba(255,255,255,.22);margin-bottom:8px;font-family:'DM Sans',sans-serif;
# }
# .divider{height:1px;
#     background:linear-gradient(90deg,transparent,rgba(99,102,241,.18),rgba(219,39,119,.18),transparent);
#     margin:0 32px;}

# /* result box */
# .rbox{padding:24px 26px 22px;border-radius:14px;text-align:center;
#     margin-top:20px;position:relative;overflow:hidden;max-width:800px;margin-left:auto;margin-right:auto;}
# .rbox::before{content:'';position:absolute;inset:0;
#     background:radial-gradient(ellipse 60% 50% at 50% 0%,rgba(255,255,255,.035),transparent);}
# .rbox.low   {background:rgba(34,197,94,.07);border:1px solid rgba(34,197,94,.2);color:#86efac;}
# .rbox.medium{background:rgba(251,191,36,.07);border:1px solid rgba(251,191,36,.2);color:#fde68a;}
# .rbox.high  {background:rgba(239,68,68,.07);border:1px solid rgba(239,68,68,.2);color:#fca5a5;}
# .rtag{font-size:9px;font-weight:700;letter-spacing:2px;text-transform:uppercase;opacity:.45;margin-bottom:5px;font-family:'DM Sans',sans-serif;}
# .rlvl{font-family:'Syne',sans-serif;font-size:40px;font-weight:800;letter-spacing:-1px;line-height:1;margin-bottom:9px;}
# .rconf{font-size:13px;opacity:.5;font-family:'DM Sans',sans-serif;}
# .rconf strong{font-size:20px;font-weight:800;opacity:1;}
# .rbar{height:4px;background:rgba(255,255,255,.06);border-radius:4px;margin-top:16px;overflow:hidden;}
# .rbar-fill{height:100%;border-radius:4px;}
# .low .rbar-fill{background:linear-gradient(90deg,#4ade80,#22c55e);}
# .medium .rbar-fill{background:linear-gradient(90deg,#fbbf24,#f59e0b);}
# .high .rbar-fill{background:linear-gradient(90deg,#f87171,#ef4444);}

# /* features */
# .features-wrap{max-width:800px;margin:0 auto;padding:0 20px 32px;}
# .features-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;}
# .feat{background:rgba(255,255,255,.02);border:1px solid rgba(255,255,255,.055);
#     border-radius:13px;padding:16px 16px 14px;}
# .feat-icon{font-size:17px;margin-bottom:7px;}
# .feat-title{font-family:'Syne',sans-serif;font-size:12.5px;font-weight:700;color:#e8eaf6;margin-bottom:3px;}
# .feat-desc{font-size:11px;color:rgba(255,255,255,.25);line-height:1.6;font-family:'DM Sans',sans-serif;}
# .footer-txt{text-align:center;padding:20px;font-size:11px;color:rgba(255,255,255,.11);
#     border-top:1px solid rgba(255,255,255,.045);letter-spacing:.3px;font-family:'DM Sans',sans-serif;}
# .footer-txt span{color:rgba(99,102,241,.4);}

# [data-testid="stVerticalBlock"]{gap:0!important;}
# [data-testid="element-container"]{margin:0!important;}
# div.stTextArea{margin-bottom:0!important;}
# div.stTextArea > label{display:none!important;}
# div.stFileUploader > label{display:none!important;}
# </style>
# <link href="https://fonts.googleapis.com/css2?family=Syne:wght@500;700;800&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet">
# """, unsafe_allow_html=True)

# # ── NLTK ───────────────────────────────────────────────────────────────────────
# @st.cache_resource(show_spinner=False)
# def download_nltk():
#     path = os.path.join(os.getcwd(), "nltk_data")
#     os.makedirs(path, exist_ok=True)
#     nltk.data.path.append(path)
#     for pkg in ["punkt","punkt_tab","stopwords","wordnet","omw-1.4"]:
#         try: nltk.data.find(pkg)
#         except: nltk.download(pkg, download_dir=path)
# download_nltk()

# @st.cache_resource
# def load_models():
#     return joblib.load("risk_model.pkl"), joblib.load("tfidf_vectorizer.pkl"), joblib.load("label_encoder.pkl")
# model, vectorizer, le = load_models()

# _sw = set(stopwords.words("english")) - {"shall","not","may","must"}
# _lm = WordNetLemmatizer()
# def preprocess(text):
#     text = re.sub(r"[^a-zA-Z\s]","",text.lower())
#     return " ".join(_lm.lemmatize(w) for w in word_tokenize(text) if w not in _sw)

# def run_model(text):
#     cleaned = preprocess(text)
#     vec = vectorizer.transform([cleaned])
#     pred = model.predict(vec)
#     probs = model.predict_proba(vec)[0]
#     classes = le.classes_
#     prob_dict = {classes[i].lower(): round(probs[i] * 100, 2) for i in range(len(classes))}
#     label = le.inverse_transform(pred)[0]
#     conf = round(max(probs) * 100, 2)
#     return {"label": label.lower(), "confidence": conf, "all_probs": prob_dict}

# for k,v in {"result":None}.items():
#     if k not in st.session_state: st.session_state[k] = v

# # ══════════════════════════════════════════════════════════════════════════════
# # HERO — full visual, no inputs
# # ══════════════════════════════════════════════════════════════════════════════
# components.html("""<!DOCTYPE html>
# <html lang="en"><head>
# <meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
# <link href="https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@300;400&display=swap" rel="stylesheet">
# <style>
# *,*::before,*::after{box-sizing:border-box;margin:0;padding:0;}
# body{background:#06060f;font-family:'DM Sans',sans-serif;color:#dde1f0;overflow:hidden;-webkit-font-smoothing:antialiased;}
# body::after{content:'';position:fixed;inset:0;pointer-events:none;
#   background-image:url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.035'/%3E%3C/svg%3E");opacity:.4;}



# .hero{position:relative;width:100%;
#   display:flex;flex-direction:column;align-items:center;justify-content:center;
#   padding:100px 20px 60px;overflow:hidden;}
# .hero::after{content:'';position:absolute;width:900px;height:550px;
#   top:-180px;left:50%;transform:translateX(-50%);
#   background:radial-gradient(ellipse,rgba(85,88,227,.17) 0%,transparent 65%);pointer-events:none;z-index:0;}
# .hero::before{content:'';position:absolute;inset:0;
#   background-image:radial-gradient(circle,rgba(165,180,252,.16) 1px,transparent 1px);
#   background-size:26px 26px;
#   mask-image:radial-gradient(ellipse 80% 55% at 50% 18%,black 15%,transparent 75%);
#   -webkit-mask-image:radial-gradient(ellipse 80% 55% at 50% 18%,black 15%,transparent 75%);}
# .orb{position:absolute;border-radius:50%;filter:blur(88px);pointer-events:none;}
# .o1{width:460px;height:460px;opacity:.11;background:radial-gradient(circle,#6366f1,transparent 65%);top:-130px;left:-70px;animation:fl 16s ease-in-out infinite;}
# .o2{width:380px;height:380px;opacity:.09;background:radial-gradient(circle,#db2777,transparent 65%);top:-50px;right:-50px;animation:fl 19s ease-in-out infinite reverse;}
# .o3{width:300px;height:300px;opacity:.08;background:radial-gradient(circle,#0891b2,transparent 65%);bottom:0;left:42%;animation:fl 23s ease-in-out infinite 5s;}
# @keyframes fl{0%,100%{transform:translate(0,0)}40%{transform:translate(22px,-30px)}70%{transform:translate(-13px,16px)}}

# @keyframes riseUp{from{opacity:0;transform:translateY(32px);}to{opacity:1;transform:translateY(0);}}
# .badge{animation:riseUp .6s cubic-bezier(.22,1,.36,1) .05s both;}
# .hl   {animation:riseUp .6s cubic-bezier(.22,1,.36,1) .18s both;}
# .sub  {animation:riseUp .6s cubic-bezier(.22,1,.36,1) .30s both;}
# .cw   {animation:riseUp .6s cubic-bezier(.22,1,.36,1) .44s both;}
# .stats{animation:riseUp .6s cubic-bezier(.22,1,.36,1) .58s both;}

# .badge{position:relative;z-index:2;display:inline-flex;align-items:center;gap:7px;
#   font-size:10px;font-weight:600;letter-spacing:1.6px;text-transform:uppercase;color:#a5b4fc;
#   background:rgba(99,102,241,.08);border:1px solid rgba(99,102,241,.2);
#   border-radius:50px;padding:5px 13px;margin-bottom:12px;}
# .bdot{width:5px;height:5px;border-radius:50%;background:#818cf8;
#   box-shadow:0 0 6px #818cf8;animation:bp 2.2s ease-in-out infinite;}
# @keyframes bp{0%,100%{opacity:1;transform:scale(1)}50%{opacity:.2;transform:scale(.55)}}

# .hl{font-family:'Syne',sans-serif;font-size:clamp(36px,5.2vw,72px);font-weight:800;
#   line-height:1.06;letter-spacing:-2.5px;text-align:center;color:#f0f2ff;
#   position:relative;z-index:2;margin-bottom:6px;}
# .grad{background:linear-gradient(95deg,#818cf8 0%,#e879f9 45%,#34d399 100%);
#   background-size:250%;-webkit-background-clip:text;-webkit-text-fill-color:transparent;
#   animation:sh 6s ease-in-out infinite;}
# @keyframes sh{0%,100%{background-position:0%}50%{background-position:100%}}
# .sub{font-size:clamp(13.5px,1.6vw,16.5px);color:rgba(220,224,255,.36);
#   font-weight:300;text-align:center;max-width:460px;line-height:1.85;
#   position:relative;z-index:2;margin:0 auto 20px;}

# .cw{position:relative;z-index:2;width:100%;max-width:800px;margin:0 auto;}
# .cglow{position:absolute;inset:-2px;
#   background:conic-gradient(from 180deg at 50% 50%,#6366f1,#db2777,#0891b2,#6366f1);
#   border-radius:24px;opacity:.22;filter:blur(18px);z-index:-1;animation:cspin 8s linear infinite;}
# @keyframes cspin{to{transform:rotate(360deg)}}
# .card{background:rgba(10,10,20,.97);border:1px solid rgba(255,255,255,.07);
#   border-radius:22px;padding:5px;box-shadow:0 28px 70px rgba(0,0,0,.8);}
# .ci{background:#080815;border-radius:18px;padding:20px 24px;}
# .tbar{display:flex;gap:7px;align-items:center;margin-bottom:13px;}
# .dot{width:11px;height:11px;border-radius:50%;}
# .dr{background:#ff5f57;}.dy{background:#febc2e;}.dg{background:#28c840;}
# .fn{font-size:10px;color:rgba(255,255,255,.14);margin-left:auto;letter-spacing:.4px;font-family:monospace;}
# .code-block{display:grid;grid-template-columns:24px 1fr;gap:0 10px;
#   font-size:12px;font-family:monospace;line-height:1.95;
#   background:rgba(99,102,241,.04);border:1px solid rgba(99,102,241,.09);
#   border-radius:10px;padding:13px 15px;margin-bottom:14px;}
# .ln{color:rgba(255,255,255,.1);text-align:right;user-select:none;font-size:10.5px;}
# .lc{color:rgba(220,224,255,.36);}
# .lc .kw{color:#a5b4fc;}.lc .st{color:#f9a8d4;}
# .rrow{display:flex;align-items:center;justify-content:space-between;gap:10px;flex-wrap:wrap;}
# .rpill{display:inline-flex;align-items:center;gap:8px;padding:9px 17px;border-radius:10px;
#   font-family:'Syne',sans-serif;font-weight:700;font-size:12.5px;
#   background:rgba(239,68,68,.1);border:1px solid rgba(239,68,68,.26);color:#fca5a5;}
# .cbox{text-align:right;}
# .cbox-label{font-size:9.5px;color:rgba(255,255,255,.22);letter-spacing:.5px;text-transform:uppercase;margin-bottom:1px;}
# .cbox-val{font-family:'Syne',sans-serif;font-size:24px;font-weight:800;color:#34d399;line-height:1;}

# .stats{display:flex;width:100%;max-width:800px;margin-top:16px;position:relative;z-index:2;
#   background:rgba(255,255,255,.02);border:1px solid rgba(255,255,255,.055);
#   border-radius:12px;overflow:hidden;}
# .stat{text-align:center;padding:15px 30px;flex:1;}
# .stat+.stat{border-left:1px solid rgba(255,255,255,.055);}
# .sn{font-family:'Syne',sans-serif;font-size:26px;font-weight:800;
#   background:linear-gradient(135deg,#c7d2fe,#f9a8d4);
#   -webkit-background-clip:text;-webkit-text-fill-color:transparent;line-height:1;}
# .sl{font-size:9.5px;color:rgba(255,255,255,.2);margin-top:3px;letter-spacing:.7px;text-transform:uppercase;}
# </style></head><body>

# <section class="hero">
#   <div class="orb o1"></div><div class="orb o2"></div><div class="orb o3"></div>
#   <div class="badge"><span class="bdot"></span>AI-Powered Legal Intelligence</div>
#   <h1 class="hl">Know Your Risk<br><span class="grad">Before You Sign</span></h1>
#   <p class="sub">Instant clause analysis. Surface hidden liabilities and get real-time confidence scores in seconds.</p>
#   <div class="cw">
#     <div class="cglow"></div>
#     <div class="card"><div class="ci">
#       <div class="tbar">
#         <div class="dot dr"></div><div class="dot dy"></div><div class="dot dg"></div>
#         <span class="fn">clause_analysis.txt — LexAI v2.1</span>
#       </div>
#       <div class="code-block">
#         <span class="ln">1</span><span class="lc"><span class="kw">§ 14.3</span> Indemnification Clause</span>
#         <span class="ln">2</span><span class="lc">The Client shall <span class="kw">indemnify, defend</span> and <span class="kw">hold harmless</span></span>
#         <span class="ln">3</span><span class="lc">the Vendor from <span class="st">any and all claims, liabilities,</span></span>
#         <span class="ln">4</span><span class="lc"><span class="st">damages, losses</span> including attorneys' fees arising from</span>
#         <span class="ln">5</span><span class="lc"><span class="kw">Client's use</span> or infringement of intellectual property…</span>
#       </div>
#       <div class="rrow">
#         <div class="rpill">🔴 HIGH RISK DETECTED</div>
#         <div class="cbox"><div class="cbox-label">Confidence</div><div class="cbox-val">94.7%</div></div>
#       </div>
#     </div></div>
#   </div>
#   <div class="stats">
#     <div class="stat"><div class="sn">10K+</div><div class="sl">Clauses Analysed</div></div>
#     <div class="stat"><div class="sn">97%</div><div class="sl">Accuracy</div></div>
#     <div class="stat"><div class="sn">&lt;2s</div><div class="sl">Per Analysis</div></div>
#   </div>
# </section>
# </body></html>""", height=780, scrolling=False)

# # ══════════════════════════════════════════════════════════════════════════════
# # ANALYSER — 100% native Streamlit widgets, fully functional
# # ══════════════════════════════════════════════════════════════════════════════
# st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# st.markdown("""
# <div class="analyser-wrap">
#   <div class="sec-eyebrow">⚡ Live Analysis Engine</div>
#   <div class="sec-title">Analyse a Contract Clause</div>
#   <div class="sec-sub">Paste text or upload a PDF — indemnification, liability, IP, termination — instant risk verdict.</div>
# </div>""", unsafe_allow_html=True)

# # Centered input container
# col1, col2, col3 = st.columns([1, 3, 1])
# with col2:
#     tab_text, tab_pdf = st.tabs(["✏️  Paste Text", "📄  Upload PDF"])

#     with tab_text:
#         st.markdown('<div style="height:12px"></div>', unsafe_allow_html=True)
#         clause = st.text_area(
#             "clause",
#             placeholder="e.g. The Client shall indemnify and hold harmless the Vendor from any claims, liabilities, damages…",
#             height=160,
#             label_visibility="collapsed"
#         )
#         # Quick-fill chips via HTML buttons that update session state
#         st.markdown("""
#         <div style="display:flex;flex-wrap:wrap;gap:6px;margin:8px 0 14px;">
#           <span style="font-size:10px;padding:3px 10px;background:rgba(99,102,241,.06);border:1px solid rgba(99,102,241,.12);border-radius:50px;color:rgba(165,180,252,.55);">💡 Tip: Paste any real contract clause above</span>
#         </div>""", unsafe_allow_html=True)
#         analyse_text = st.button("⚡  Analyse Risk", key="btn_text", use_container_width=True)

#     with tab_pdf:
#         st.markdown('<div style="height:12px"></div>', unsafe_allow_html=True)
#         uploaded = st.file_uploader(
#             "pdf",
#             type=["pdf"],
#             label_visibility="collapsed",
#             help="Upload a contract PDF — text will be extracted automatically"
#         )
#         if uploaded:
#             st.markdown(f"""
#             <div style="display:flex;align-items:center;gap:8px;padding:10px 14px;
#               border-radius:9px;background:rgba(34,197,94,.06);
#               border:1px solid rgba(34,197,94,.18);color:#86efac;
#               font-size:12.5px;margin-bottom:12px;">
#               ✅ <strong>{uploaded.name}</strong> ready for analysis
#             </div>""", unsafe_allow_html=True)
#         analyse_pdf = st.button("⚡  Analyse PDF", key="btn_pdf", use_container_width=True)

# # ── Process text ───────────────────────────────────────────────────────────────
# if analyse_text:
#     if not clause or not clause.strip():
#         st.warning("⚠️ Please paste a contract clause before analysing.")
#     else:
#         with st.spinner("Analysing clause…"):
#             st.session_state.result = run_model(clause.strip())
#         st.rerun()

# # ── Process PDF ────────────────────────────────────────────────────────────────
# if analyse_pdf:
#     if uploaded is None:
#         st.warning("⚠️ Please upload a PDF file before analysing.")
#     else:
#         with st.spinner("Extracting text and analysing…"):
#             try:
#                 reader = PyPDF2.PdfReader(io.BytesIO(uploaded.read()))
#                 pdf_text = ""
#                 for page in reader.pages:
#                     t = page.extract_text()
#                     if t: pdf_text += t + "\n"
#                 if not pdf_text.strip():
#                     st.error("❌ Could not extract text. Make sure the PDF is text-based, not a scanned image.")
#                 else:
#                     st.session_state.result = run_model(pdf_text.strip())
#                     st.rerun()
#             except Exception as e:
#                 st.error(f"❌ Error reading PDF: {e}")

# # ── Show result ─────────────────────────────────────────────────────────────────
# if st.session_state.result:
#     R = st.session_state.result
#     icons = {"low":"🟢","medium":"🟡","high":"🔴"}
#     icon = icons.get(R["label"],"⚪")
#     bar_colors = {
#         "low":   "linear-gradient(90deg,#4ade80,#22c55e)",
#         "medium":"linear-gradient(90deg,#fbbf24,#f59e0b)",
#         "high":  "linear-gradient(90deg,#f87171,#ef4444)",
#     }
#     insights = {
#         "low": "This clause appears standard with minimal risk. Proceed with normal review.",
#         "medium": "Potential concerns detected. Review the wording for ambiguity or over-reaching terms.",
#         "high": "Critical risk detected! This clause contains significant liabilities or unfavorable terms."
#     }
    
#     _, rc, _ = st.columns([1,3,1])
#     with rc:
#         st.markdown(f"""
#         <div class="rbox {R['label']}">
#           <div class="rtag">Risk Assessment</div>
#           <div class="rlvl">{icon} {R['label'].upper()} RISK</div>
#           <div class="rconf">Confidence: <strong>{R['confidence']}%</strong></div>
#           <div class="rbar">
#             <div class="rbar-fill" style="width:{R['confidence']}%;background:{bar_colors[R['label']]};"></div>
#           </div>
#           <div style="margin-top:20px;padding-top:15px;border-top:1px solid rgba(255,255,255,.05);text-align:left;">
#             <div style="font-size:10px;text-transform:uppercase;letter-spacing:1px;color:rgba(255,255,255,.3);margin-bottom:10px;">Probability Breakdown</div>
#             <div style="display:flex;justify-content:space-between;font-size:12px;margin-bottom:5px;">
#               <span>Low Risk</span><span style="color:#86efac;">{R['all_probs'].get('low', 0)}%</span>
#             </div>
#             <div style="display:flex;justify-content:space-between;font-size:12px;margin-bottom:5px;">
#               <span>Medium Risk</span><span style="color:#fde68a;">{R['all_probs'].get('medium', 0)}%</span>
#             </div>
#             <div style="display:flex;justify-content:space-between;font-size:12px;margin-bottom:5px;">
#               <span>High Risk</span><span style="color:#fca5a5;">{R['all_probs'].get('high', 0)}%</span>
#             </div>
#           </div>
#           <div style="margin-top:15px;padding:12px;background:rgba(255,255,255,.03);border-radius:8px;font-size:13px;text-align:left;color:rgba(255,255,255,.6);border:1px solid rgba(255,255,255,.05);">
#             <strong>Insight:</strong> {insights.get(R['label'])}
#           </div>
#         </div>""", unsafe_allow_html=True)

# # ── Divider + Features ──────────────────────────────────────────────────────────
# st.markdown("""
# <div class="divider" style="margin-top:32px;"></div>
# <div class="features-wrap" style="margin-top:28px;">
#   <div class="features-grid">
#     <div class="feat"><div class="feat-icon">🧠</div>
#       <div class="feat-title">ML Risk Classification</div>
#       <div class="feat-desc">TF-IDF + trained classifier detects Low, Medium & High risk clauses with precision.</div></div>
#     <div class="feat"><div class="feat-icon">📊</div>
#       <div class="feat-title">Confidence Scoring</div>
#       <div class="feat-desc">Probability-based score on every result so you know how certain the model is.</div></div>
#     <div class="feat"><div class="feat-icon">⚡</div>
#       <div class="feat-title">Instant Results</div>
#       <div class="feat-desc">Analysis in under 2 seconds — no external servers, fully local inference.</div></div>
#   </div>
# </div>
# <div class="footer-txt">© 2026 <span>LexAI</span> · Contractual Risk Intelligence · Powered by Streamlit</div>
# """, unsafe_allow_html=True)


# import streamlit as st
# from rag.retriever import retrieve
# from rag.llm_rag import generate_response

# st.set_page_config(page_title="Contract Risk Analyzer")

# st.title("📄 Intelligent Contract Risk Analyzer")
# st.write("RAG + LLM based legal clause risk analysis")

# clause = st.text_area("Enter contract clause:")

# if st.button("Analyze"):

#     if clause.strip() == "":
#         st.warning("Please enter a clause")

#     else:
#         with st.spinner("🔍 Retrieving similar clauses..."):
#             docs = retrieve(clause)

#         st.subheader("🔍 Retrieved Clauses")

#         for d in docs:
#             st.write(f"**Clause:** {d['clause']}")
#             st.write(f"Type: {d['type']} | Risk: {d['risk']}")
#             st.write("---")

#         with st.spinner("🧠 AI reasoning..."):
#             result = generate_response(clause, docs)

#         st.subheader("⚠️ AI Risk Analysis")
#         st.success(result)


import streamlit as st
from agent.graph import build_agent
from utils.parser import extract_text_from_pdf

# Initialize agent
agent = build_agent()

st.set_page_config(page_title="Contract Risk Analyzer", layout="wide")

st.title("📄 Intelligent Contract Risk Analyzer")
st.write("RAG + LLM + Agentic AI based legal contract analysis")

# ---- INPUT SECTION ----
st.subheader("📥 Input")

option = st.radio("Choose input type:", ["Enter Text", "Upload PDF"])

contract_text = ""

if option == "Enter Text":
    contract_text = st.text_area("Enter contract text:")

elif option == "Upload PDF":
    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

    if uploaded_file:
        contract_text = extract_text_from_pdf(uploaded_file)
        st.success("✅ PDF processed successfully")

# ---- ANALYZE BUTTON ----
if st.button("🚀 Analyze Contract"):

    if not contract_text.strip():
        st.warning("Please provide contract text or upload a PDF.")
    else:
        with st.spinner("🤖 Agent analyzing contract..."):
            result = agent.invoke({"text": contract_text})

        report = result["report"]

        st.subheader("📊 Risk Analysis Report")
        st.text(report)

        # ---- DOWNLOAD BUTTON ----
        st.download_button(
            label="📄 Download Report",
            data=report,
            file_name="contract_risk_report.txt",
            mime="text/plain"
        )

# ---- DISCLAIMER ----
st.markdown("---")
st.caption("⚠️ This analysis is AI-generated and does not constitute legal advice.")