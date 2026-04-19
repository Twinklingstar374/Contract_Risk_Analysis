# ⚖️ Intelligent Contract Risk Analysis using RAG & Agentic AI

## 🚀 From ML Classification to Agentic Legal Reasoning

---

## 📌 Project Overview

This project presents an **AI-powered system for analyzing legal contracts** and identifying potential risks at the clause level.

It evolves from a traditional Machine Learning approach to a modern **Agentic AI system** that combines:

* Retrieval-Augmented Generation (RAG)
* Large Language Models (LLMs)
* LangGraph-based agent workflows

The system not only predicts risk but also provides **explanations and contextual insights**.

---

## 🧠 Key Features

* 📄 Upload contract (PDF) or paste text
* 🔍 Clause-level risk analysis
* ⚠️ Risk classification (High / Medium / Low)
* 📚 Context retrieval using FAISS (RAG)
* 🧠 LLM-based reasoning (Groq API)
* 🔁 Agentic workflow using LangGraph
* 📊 Structured risk report
* 🌐 Deployed using Streamlit

---

## 🚀 How It Works

```text
Input (PDF/Text)
        ↓
Clause Segmentation (utils/parser.py)
        ↓
RAG Retrieval (rag/retriever.py)
        ↓
LLM Reasoning (rag/llm_rag.py)
        ↓
Agent Workflow (agent/graph.py)
        ↓
Final Risk Report
```

---

## 📊 Milestone 1: ML-Based Risk Classification

### 🔹 Approach

* Text preprocessing (cleaning, tokenization)
* Feature extraction using TF-IDF
* Model: Logistic Regression

### 🔹 Files

* `risk_model.pkl`
* `label_encoder.pkl`
* `tfidf_vectorizer.pkl`

### 🔹 Output

* Risk classification (High / Medium / Low)

### 🔹 Limitation

* No explanation or reasoning
* No contextual understanding

---

## 🚀 Milestone 2: Agentic AI + RAG System

### 🔹 1. Clause Segmentation

* Implemented in `utils/parser.py`
* Splits contracts into structured clauses

---

### 🔹 2. RAG Pipeline

* Embeddings: sentence-transformers
* Vector store: FAISS
* Files:

  * `faiss.index`
  * `metadata.pkl`
  * `build_index.py`

```text
Query → Embedding → Similar Clauses → Context
```

---

### 🔹 3. LLM Reasoning

* Implemented in `rag/llm_rag.py`
* Uses Groq API
* Generates:

  * Risk level
  * Explanation
  * Recommendation

---

### 🔹 4. Agentic Workflow (LangGraph)

* Implemented in `agent/graph.py`

```text
Extract → Analyze → Loop → Report
```

* Processes clauses iteratively
* Maintains state
* Generates final report

---

## 🖥️ User Interface

Built using **Streamlit (`app.py`)**

### Features:

* Upload PDF or paste text
* View contract content
* Risk dashboard
* Clause-level results
* Export report

---

## 🌐 Deployment

Deployed on Streamlit Cloud

🔗 **Live App:** [https://your-app-link.streamlit.app](https://contractriskanalysis-l3qvfbvsojfij8hek3khzk.streamlit.app/)

---

## ⚙️ Tech Stack

### 🔹 NLP & ML

* scikit-learn
* nltk
* TF-IDF

### 🔹 RAG

* sentence-transformers
* FAISS

### 🔹 Agentic AI

* LangGraph
* LangChain

### 🔹 LLM

* Groq API

### 🔹 Frontend

* Streamlit

### 🔹 Others

* PyPDF
* pandas, numpy

---

## 📁 Project Structure

```text
Contract_Risk_Analysis/
│
├── app.py
├── requirements.txt
├── README.md
│
├── agent/
│   └── graph.py
│
├── rag/
│   ├── retriever.py
│   ├── llm_rag.py
│   ├── build_index.py
│   ├── faiss.index
│   └── metadata.pkl
│
├── utils/
│   └── parser.py
│
├── risk_model.pkl
├── label_encoder.pkl
├── tfidf_vectorizer.pkl
```

---

## 🔐 Environment Setup

Create `.streamlit/secrets.toml`:

```text
GROQ_API_KEY = "your_api_key_here"
```

---

## ▶️ Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

---

## 📊 Evaluation Alignment

✔ RAG implementation
✔ Agentic AI (LangGraph)
✔ LLM-based reasoning
✔ Clean architecture
✔ Deployed UI
✔ Explainable outputs

---

## ⚠️ Disclaimer

This system provides AI-generated insights and **does not constitute legal advice**.

---

## 👥 Team Members

* Bulbul Agarwalla
* Ganga Raghuwanshi
* Anuradha Raghuwanshi
* Alisha Gupta

---

## 🎯 Future Work

* Clause type classification
* Highlight clauses in PDF
* Multi-contract comparison
* Fine-tuned legal LLM

---

## 🧠 Key Insight

> This project demonstrates how RAG combined with agentic workflows enables explainable, context-aware contract analysis beyond traditional ML approaches.


