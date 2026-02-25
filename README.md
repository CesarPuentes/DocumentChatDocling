
### This in a exercise from the IBM course: Chat with your documents via Agentic RAG, LangGraph, Docling

Link: https://cognitiveclass.ai/courses/chat-with-your-documents-via-agentic-rag-langgraph-docling

# **DocChat** 📝🤖  
🚀 **AI-powered Multi-Agent RAG system for intelligent document querying with fact verification**  

![DocChat Cover Image](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/zSuj0yrlvjcVkkbW4frkNA/docchat-landing-page.png)

---

## **📌 Overview**  

**DocChat** is a **multi-agent Retrieval-Augmented Generation (RAG) system** designed to help users query **long, complex documents** with **accurate, fact-verified answers**. Unlike traditional chatbots like **ChatGPT or DeepSeek**, which **hallucinate responses and struggle with structured data**, DocChat **retrieves, verifies, and corrects** answers before delivering them.  

💡 **Key Features:**  
✅ **Multi-Agent System** – A **Research Agent** generates answers, while a **Verification Agent** fact-checks responses.  
✅ **Hybrid Retrieval** – Uses **BM25 and vector search** to find the most relevant content.  
✅ **Handles Multiple Documents** – Selects the most relevant document even when multiple files are uploaded.  
✅ **Scope Detection** – Prevents hallucinations by **rejecting irrelevant queries**.  
✅ **Fact Verification** – Ensures responses are accurate before presenting them to the user.  
✅ **Web Interface with Gradio** – Allowing seamless document upload and question-answering.  

---

## **🎥 Demo Video**  

📹 **[Click here to watch the DocChat demo](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/zyARt3f3bnm5T-6C4AE3mw/docchat-demo.mp4)**  
*(Opens in a new tab)*

---

## **🛠️ How DocChat Works**  

### **1️⃣ Query Processing & Scope Analysis**  
- Users **upload documents** and **ask a question**.  
- DocChat **analyzes query relevance** and determines if the question is **within scope**.  
- If the query is **irrelevant**, DocChat **rejects it** instead of generating hallucinated responses.  

### **2️⃣ Multi-Agent Research & Retrieval**  
- **Docling** parses documents into a structured format (Markdown, JSON).  
- **LangChain & ChromaDB** handle **hybrid retrieval** (BM25 + vector embeddings).  
- Even when **multiple documents** are uploaded, **DocChat finds the most relevant sections** dynamically.  

### **3️⃣ Answer Generation & Verification**  
- **Research Agent** generates an answer using retrieved content.  
- **Verification Agent** cross-checks the response against the source document.  
- If **verification fails**, a **self-correction loop** re-runs retrieval and research.  

### **4️⃣ Response Finalization**  
- **If the answer passes verification**, it is displayed to the user.  
- **If the question is out of scope**, DocChat informs the user instead of hallucinating.  

---

## **🎯 Why Use DocChat Instead of ChatGPT or DeepSeek?**  

| Feature | **ChatGPT/DeepSeek** ❌ | **DocChat** ✅ |
|---------|-----------------|---------|
| Retrieves from uploaded documents | ❌ No | ✅ Yes |
| Handles multiple documents | ❌ No | ✅ Yes |
| Extracts structured data from PDFs | ❌ No | ✅ Yes |
| Prevents hallucinations | ❌ No | ✅ Yes |
| Fact-checks answers | ❌ No | ✅ Yes |
| Detects out-of-scope queries | ❌ No | ✅ Yes |

🚀 **DocChat is built for enterprise-grade document intelligence, research, and compliance workflows.**  

---

## **📦 Installation**  

### **1️⃣ Clone the Repository**  
```bash
git clone https://github.com/HaileyTQuach/docchat-docling.git docchat
cd docchat
```

### **2️⃣ Set Up Virtual Environment**  
```bash
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### **3️⃣ Install Dependencies**  
```bash
pip install -r requirements.txt
```

### **4️⃣ Configuration & LLM Providers**  
DocChat uses a unified abstraction layer. Create a `.env` file (use `.env.example` as a template):

```bash
cp .env.example .env
```

#### **Global Settings**
| Variable | Description | Default |
|----------|-------------|---------|
| `LLM_PROVIDER` | Active provider (`watsonx`, `deepseek`, `openai`, `ollama`) | `watsonx` |
| `LOG_LEVEL` | Logging detail (`INFO`, `DEBUG`, `ERROR`) | `INFO` |

#### **Provider-Specific Setup**

**1. IBM WatsonX (Enterprise)**
- `WATSONX_APIKEY`: Your IBM Cloud IAM API key.
- `WATSONX_PROJECT_ID`: Your WatsonX Project GUID (found in Project -> Manage -> General).
- *Embeddings:* Automatically uses `ibm/slate-125m-english-rtrvr-v2`.

**2. DeepSeek (Performance/Cost)**
- `DEEPSEEK_API_KEY`: Your DeepSeek API key.
- `DEEPSEEK_MODEL_NAME`: Set to `deepseek-chat` or `deepseek-reasoner`.
- *Embeddings:* Automatically uses DeepSeek's embedding API.

**3. OpenAI (Standard)**
- `OPENAI_API_KEY`: Your OpenAI API key.
- `OPENAI_MODEL_NAME`: e.g., `gpt-4o-mini`.

**4. Ollama (Local/Privacy)**
- `OLLAMA_MODEL_NAME`: The model tag (e.g., `llama3`, `mistral`).
- `OLLAMA_BASE_URL`: Usually `http://localhost:11434/v1`.
- *Note:* Ensure Ollama is running locally and the model is pulled (`ollama pull llama3`).

---

#### **Advanced Configuration (Optional)**
| Variable | Description | Default |
|----------|-------------|---------|
| `VECTOR_SEARCH_K` | Number of documents to retrieve via vector search | `10` |
| `CHROMA_DB_PATH` | Local directory for vector database | `./chroma_db` |
| `MAX_FILE_SIZE` | Maximum upload size in MB | `5` |
| `ALLOWED_EXTENSIONS` | Supported file types | `.pdf`, `.docx`, `.txt` |

---

### **5️⃣ Run the Application** 
```bash
python app.py
```

DocChat will be accessible at `http://0.0.0.0:7860`.


## 🖥️ Usage Guide  

1️⃣ **Upload one or more documents** (PDF, DOCX, TXT, Markdown).  

2️⃣ **Enter a question** related to the document.  

3️⃣ **Click "Submit"** – DocChat retrieves, analyzes, and verifies the response.  

4️⃣ **Review the answer & verification report** for confidence.  

5️⃣ **If the question is out of scope**, DocChat will inform you instead of fabricating an answer.  


## 🤝 Contributing  

Want to **improve DocChat**? Feel free to:  

- **Fork the repo**  
- **Create a new branch** (`feature-xyz`)  
- **Commit your changes**  
- **Submit a PR (Pull Request)**  

We welcome contributions from **AI/NLP enthusiasts, researchers, and developers!** 🚀  

---

## 📜 License  

This project is licensed under a Customed Non-Commercial License – check LICENSE for more details.

---

## 💬 Contact & Support  

📧 **Email:** [hailey@haileyq.com]  


