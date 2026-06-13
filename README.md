# 🤖 AI Chatbot with RAG, Tools & Streaming UI

An AI-powered chatbot built using **LangGraph + LangChain** that supports real-time conversations, PDF-based retrieval (RAG), and tool integration (calculator, stock data, and web search).

It features a modular backend, streaming UI with Streamlit, and persistent multi-session chat memory.

---

## 🚀 Features

* 💬 LLM-powered chatbot (Groq + Llama 3)
* 📄 RAG over PDFs (FAISS + embeddings)
* 🛠️ Tool integration:

  * Calculator
  * Stock price API
  * Web search (DuckDuckGo)
* ⚡ Real-time streaming responses
* 🧠 Multi-session chat with persistent memory (thread-based)
* 📂 Modular backend architecture (clean separation of concerns)
* 🎯 Interactive Streamlit UI

---

## 🏗️ Tech Stack

* **LLM & Agents**: LangChain, LangGraph
* **Model Provider**: Groq (Llama 3)
* **Vector Store**: FAISS
* **Embeddings**: Ollama
* **Frontend**: Streamlit
* **Backend**: Python (modular architecture)
* **Database**: SQLite (chat memory)

---

## 📂 Project Structure

```
AI_CHATBOT/
├── backend/
│   ├── __init__.py
│   └── app/
│       ├── __init__.py
│       ├── config.py        # Environment & settings
│       ├── core.py          # LLM + embeddings setup
│       ├── tools.py         # All tools (calculator, stock, search, RAG)
│       ├── rag_store.py     # PDF ingestion + retriever storage
│       ├── graph.py         # LangGraph workflow (state + nodes)
│       └── service.py       # Interface layer for frontend
│
├── frontend/
│   ├── app.py               # Main Streamlit app
│   ├── sidebar.py          # Sidebar UI (threads + uploads)
│   └── chat_area.py        # Chat rendering + streaming
│
├── data/
│   └── chatbot.db          # SQLite database
│
├── .env
├── requirements.txt
├── README.md
└── .gitignore
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the repository

```bash
git clone https://github.com/<your-username>/ai-chatbot-rag.git
cd ai-chatbot-rag
```

---

### 2️⃣ Create environment (recommended)

Using conda:

```bash
conda create -n chatbot python=3.10 -y
conda activate chatbot
```

Or using venv:

```bash
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```

---

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Add environment variables

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key
```

---

### 5️⃣ Run the app (IMPORTANT: from project root)

```bash
streamlit run frontend/app.py
```

---

## 🧠 How It Works

1. User enters a query via Streamlit UI

2. LangGraph agent decides:

   * Direct LLM response
   * Tool usage
   * RAG retrieval (if PDF is uploaded)

3. For PDF queries:

   * Document is chunked
   * Stored in FAISS
   * Relevant chunks retrieved

4. Tool execution (if required):

   * Calculator
   * Stock API
   * Web search

5. Final response is generated and streamed in real-time

6. Chat history is stored using thread-based memory (SQLite)

---

## ⚡ Performance Optimizations

* Reduced chunk size for faster retrieval
* Limited top-k retrieval
* Controlled LLM token output
* Streaming responses for better UX
* Modular architecture for scalability

---

## 📸 Demo

*Add screenshots or GIFs here to showcase UI and features*

---

## 💡 Future Improvements

* 🔐 Authentication & user accounts
* ☁️ Deployment (AWS / Render / GCP)
* 📊 Observability (LangSmith)
* 🧾 Multi-format document support (PDF, DOCX, TXT)
* ⚡ Hybrid search (BM25 + vector search)
* 🧠 Memory optimization & caching

---

## 📜 License

This project is open-source and available under the MIT License.

---

## 🙌 Acknowledgements

* LangChain & LangGraph
* Groq API
* Streamlit
* FAISS
* Ollama
