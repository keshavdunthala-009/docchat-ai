# 🧠 DocChat AI — RAG-Powered Document Q&A System

<div align="center">

![DocChat AI Banner](https://img.shields.io/badge/DocChat-AI-6c47ff?style=for-the-badge&logo=brain&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.141-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-18-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**Upload any document. Ask any question. Get 100% accurate answers — grounded in your document, not hallucinated.**

[🚀 Live Demo](https://docchat-ai-delta.vercel.app) • [📦 GitHub](https://github.com/keshavdunthala-009/docchat-ai) • [🐛 Report Bug](https://github.com/keshavdunthala-009/docchat-ai/issues)

</div>

---

## 📌 What is DocChat AI?

**DocChat AI** is a production-deployed, full-stack AI application built on **Retrieval-Augmented Generation (RAG)** architecture. It allows users to upload any document (PDF, Excel, Word, PowerPoint, CSV, images) and ask questions in natural language — receiving precise, document-grounded answers powered by **Groq's Llama3-70B** large language model.

Unlike general-purpose AI chatbots that rely on pre-trained knowledge and often hallucinate, DocChat AI **reads only your uploaded document** and answers strictly from it — making every response traceable, accurate, and trustworthy.

### 🎯 Who is this for?

| User | Use Case |
|------|----------|
| 🎓 Students | Quickly extract key information from research papers, textbooks |
| 💼 Professionals | Query contracts, reports, financial documents |
| 🏥 Healthcare | Extract patient data from medical records securely |
| ⚖️ Legal | Search through lengthy legal documents instantly |
| 🏢 Enterprises | Internal document Q&A without exposing data to third parties |

---

## ✨ Features

- 📄 **Multi-format Upload** — PDF, Excel (.xlsx), Word (.docx), PowerPoint (.pptx), CSV, Images (PNG/JPG)
- 🤖 **AI-Powered Q&A** — Groq's Llama3-70B generates precise answers
- 🔒 **Per-User Isolation** — Each user gets a unique session; documents are never mixed
- 💾 **Persistent Storage** — Documents stored in Supabase; survives server restarts
- 📊 **Table Understanding** — pdfplumber extracts table structure for accurate data queries
- 🌐 **Production Deployed** — Live on Railway (backend) + Vercel (frontend)
- 🎨 **Dark Theme UI** — Professional, responsive React interface
- ⚡ **Smart RAG Mode** — Full text for small docs, chunk retrieval for large docs (1000+ pages)
- 🔐 **Zero Hallucinations** — LLM answers ONLY from your document content

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     USER BROWSER                             │
│           https://docchat-ai-delta.vercel.app                │
│                                                              │
│    ┌──────────────┐          ┌──────────────────────────┐   │
│    │   Sidebar    │          │        Chat UI            │   │
│    │  Upload Docs │          │   Ask Questions           │   │
│    └──────┬───────┘          └───────────┬──────────────┘   │
└───────────┼──────────────────────────────┼──────────────────┘
            │ POST /upload                  │ POST /ask
            ▼                              ▼
┌─────────────────────────────────────────────────────────────┐
│              RAILWAY BACKEND (FastAPI + Python)              │
│                                                              │
│   ┌────────────┐  ┌─────────────────┐  ┌────────────────┐  │
│   │  main.py   │  │  rag_pipeline   │  │ document_      │  │
│   │  REST API  │→ │  Smart RAG      │→ │ handler        │  │
│   │  Endpoints │  │  Orchestration  │  │ Multi-format   │  │
│   └────────────┘  └─────────────────┘  └────────────────┘  │
└──────────┬──────────────────┬───────────────────────────────┘
           │                  │
    ┌──────▼──────┐    ┌──────▼──────┐    ┌───────────────┐
    │  Supabase   │    │  ChromaDB   │    │   Groq API    │
    │  PostgreSQL │    │  Vector DB  │    │  Llama3-70B   │
    │  Full Text  │    │  Embeddings │    │  Answer Gen   │
    │  Persistent │    │  Similarity │    │  Zero Halluc. │
    └─────────────┘    └─────────────┘    └───────────────┘
```

---

## 🔄 How It Works — End to End

### Phase 1: Document Upload

```
User uploads PDF/Excel/Word/PPT
           ↓
File type detected automatically
           ↓
Text extracted:
  PDF      → pdfplumber (text + tables) / PyPDF2 (fallback)
  Excel    → openpyxl (all sheets)
  Word     → python-docx (paragraphs + tables)
  PPT      → python-pptx (all slides + shapes)
  CSV      → csv module
  Image    → pytesseract (OCR)
  Scanned  → pdf2image + pytesseract (OCR)
           ↓
Full text stored in Supabase (permanent)
           ↓
Text chunked into 500-char segments
           ↓
Each chunk → Sentence Transformer → 384-dim vector
           ↓
Vectors stored in ChromaDB
           ↓
✅ Upload complete
```

### Phase 2: Question Answering

```
User types: "What are the projects mentioned?"
           ↓
POST /ask with { question, session_id }
           ↓
Fetch full document from Supabase
           ↓
Smart RAG Decision:
  < 100K chars → Full text sent to LLM (100% accuracy)
  > 100K chars → Top 7 chunks retrieved via cosine similarity
           ↓
Context + Question sent to Groq API (Llama3-70B)
           ↓
LLM reads document and generates answer
           ↓
✅ Accurate answer returned to user
```

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | React 18 + Vite | User interface, dark theme |
| **Backend** | FastAPI (Python 3.12) | REST API server |
| **PDF Processing** | pdfplumber + PyPDF2 | Text & table extraction |
| **Excel/Word/PPT** | openpyxl, python-docx, python-pptx | Multi-format support |
| **OCR** | pytesseract + pdf2image | Scanned document support |
| **Embeddings** | Sentence Transformers (all-MiniLM-L6-v2) | 384-dim text vectors |
| **Vector Database** | ChromaDB | Cosine similarity search |
| **Persistent DB** | Supabase (PostgreSQL) | Document storage |
| **LLM** | Groq API — llama-3.3-70b-versatile | Answer generation |
| **Frontend Deploy** | Vercel | CDN, auto-deploy |
| **Backend Deploy** | Railway | Server hosting |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- Groq API key (free at [console.groq.com](https://console.groq.com))
- Supabase account (free at [supabase.com](https://supabase.com))

### 1. Clone the Repository

```bash
git clone https://github.com/keshavdunthala-009/docchat-ai.git
cd docchat-ai
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows
source venv/bin/activate      # Mac/Linux

# Install dependencies
pip install -r requirements.txt
```

### 3. Create Environment Variables

Create `backend/.env`:

```env
GROQ_API_KEY=your_groq_api_key_here
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_supabase_secret_key
```

### 4. Setup Supabase

Run this SQL in your Supabase SQL editor:

```sql
CREATE TABLE documents (
  id SERIAL PRIMARY KEY,
  session_id TEXT NOT NULL,
  document_name TEXT NOT NULL,
  full_text TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);
```

### 5. Frontend Setup

```bash
cd frontend
npm install
```

Create `frontend/.env`:

```env
VITE_API_URL=http://localhost:8000
```

### 6. Run the Application

**Terminal 1 — Backend:**
```bash
cd backend
python main.py
```

**Terminal 2 — Frontend:**
```bash
cd frontend
npm run dev
```

Open: [http://localhost:5173](http://localhost:5173)

---

## 📁 Project Structure

```
docchat-ai/
├── backend/
│   ├── main.py                 # FastAPI server, REST endpoints
│   ├── rag_pipeline.py         # Smart RAG orchestration
│   ├── document_handler.py     # Multi-format text extraction
│   ├── llm_answer.py           # Groq API integration
│   ├── supabase_handler.py     # Persistent document storage
│   ├── requirements.txt        # Python dependencies
│   └── Procfile                # Railway deployment config
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx             # Root component, session management
│   │   └── components/
│   │       ├── Sidebar.jsx     # Upload zone, document list, stats
│   │       └── Chat.jsx        # Chat interface, message bubbles
│   ├── package.json
│   └── vite.config.js
│
└── README.md
```

---

## 🔐 Security Architecture

```
✅ Per-user session isolation (UUID-based)
✅ API keys stored in Railway env variables (never in code)
✅ Documents stored per session in Supabase
✅ No cross-user data access possible
✅ CORS configured for authorized origins only
✅ Groq processes and forgets — data not used for training
✅ .env files excluded from GitHub via .gitignore
```

---

## 📊 Performance & Limits

| Document Size | Pages | Mode | Accuracy |
|--------------|-------|------|----------|
| < 20K chars | ~50 pages | Full Text | ✅ 100% |
| 20K–100K chars | ~250 pages | Full Text | ✅ 100% |
| 100K–500K chars | ~1000 pages | RAG Chunks | ✅ 90–95% |
| 500K+ chars | 1000+ pages | RAG Chunks | ✅ 85–90% |

---

## 🌐 Deployment

| Service | Platform | URL |
|---------|----------|-----|
| Frontend | Vercel | [docchat-ai-delta.vercel.app](https://docchat-ai-delta.vercel.app) |
| Backend | Railway | docchat-rag-llm-production.up.railway.app |
| Database | Supabase | Managed PostgreSQL |
| LLM | Groq Cloud | llama-3.3-70b-versatile |

**Total Monthly Cost: $0** ✅

---

## 🧠 Key Engineering Decisions

### Why RAG over fine-tuning?
Fine-tuning is expensive, slow, and doesn't scale to dynamic documents. RAG retrieves relevant context at query time — making it perfect for user-uploaded documents.

### Why Supabase over in-memory storage?
Railway's free tier restarts servers nightly, wiping memory. Supabase provides free, persistent PostgreSQL storage that survives restarts.

### Why Groq over OpenAI?
Groq is free, faster (specialised inference chips), and Llama3-70B delivers comparable quality to GPT-4 for document Q&A tasks.

### Why pdfplumber over PyPDF2?
PyPDF2 loses table structure. pdfplumber preserves cell-by-cell table data, enabling accurate answers for financial reports, mark sheets, etc.

---

## 🛣️ Roadmap

- [ ] OCR support for scanned PDFs (Tesseract)
- [ ] Multi-document querying (ask across multiple uploads)
- [ ] Conversation history (multi-turn chat)
- [ ] User authentication with login system
- [ ] Semantic chunking (smarter than character-based)
- [ ] Export chat history as PDF
- [ ] API rate limiting per user
- [ ] Admin dashboard for usage analytics

---

## 🤝 Contributing

Contributions are welcome!

```bash
# Fork the repo
git fork https://github.com/keshavdunthala-009/docchat-ai

# Create feature branch
git checkout -b feature/your-feature-name

# Commit changes
git commit -m "Add: your feature description"

# Push and create PR
git push origin feature/your-feature-name
```

---

## 📄 License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.

---

## 👨‍💻 Author

**Keshav Reddy Dunthala**

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?style=flat&logo=linkedin)](https://www.linkedin.com/in/keshav143)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-black?style=flat&logo=github)](https://github.com/keshavdunthala-009)
[![Email](https://img.shields.io/badge/Email-Contact-red?style=flat&logo=gmail)](mailto:Keshavreddy248@gmail.com)

---

## ⭐ Show Your Support

If this project helped you, please consider giving it a ⭐ on GitHub!

It motivates me to keep building and sharing open-source AI projects.

---

<div align="center">

**Built with ❤️ using Python, FastAPI, React, and Groq AI**

[🚀 Try Live Demo](https://docchat-ai-delta.vercel.app)

</div>
