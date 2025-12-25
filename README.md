# 🎵 Classical Music Q&A - AI-Powered Assistant

A full-stack web application that combines **HuggingFace LLMs** with **RAG (Retrieval Augmented Generation)** to create an intelligent classical music assistant. Pre-loaded with biographies of 107+ major composers from Medieval to Contemporary periods.

[![FastAPI](https://img.shields.io/badge/FastAPI-0.127.0-009688?logo=fastapi)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-19.2.0-61DAFB?logo=react)](https://reactjs.org/)
[![HuggingFace](https://img.shields.io/badge/HuggingFace-Llama_3.2-FFD21E?logo=huggingface)](https://huggingface.co/)
[![LangChain](https://img.shields.io/badge/LangChain-1.2.0-00A67E)](https://langchain.com/)

---

## ✨ Features

### 💬 **Intelligent Chat**
- Ask questions about classical composers, their lives, works, and contributions
- Context-aware responses using RAG from 107+ composer biographies
- Source citations showing which documents informed each answer
- Persistent chat history across sessions

### 📚 **Rich Knowledge Base**
- **Pre-loaded**: 107 composer biographies (5,800+ text chunks)
- **Periods Covered**: Medieval, Renaissance, Baroque, Classical, Romantic, 20th Century, Contemporary
- **Major Composers**: Bach, Mozart, Beethoven, Brahms, Stravinsky, and 102 more
- Scraped from Wikipedia, IMSLP, and AllMusic
- Automatically embedded and searchable

### 🗂️ **Session Management**
- Create, rename, and delete conversations
- Edit conversation titles inline
- Switch between multiple sessions
- Automatic session tracking
- Message deletion for conversation editing

### 🚀 **Free Deployment Ready**
- Deploy to Render with free tier
- Uses 100% free HuggingFace Inference API
- No credit card required
- Production-ready configuration included

---

## 🚀 Quick Start (Local Development)

### Prerequisites

1. **Python 3.10+**
2. **Node.js 18+**
3. **HuggingFace Account** (free) - [Sign up](https://huggingface.co/join)

### 1. Get HuggingFace API Token

1. Go to [https://huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
2. Click "New token"
3. Name it (e.g., "classical-music-app")
4. Select "Read" permission
5. Copy the token (starts with `hf_...`)

### 2. Backend Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd classical-music-qa/backend

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
echo "HF_TOKEN=hf_your_token_here" > .env

# Start the server
python run.py
```

Backend runs at: `http://localhost:8000`
API docs at: `http://localhost:8000/docs`

### 3. Frontend Setup

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev
```

Frontend runs at: `http://localhost:5173`

---

## 🌐 Deployment Options (100% Free)

### Option 1: Vercel + Render (Recommended ⭐)
- **Frontend**: Vercel (fastest, best CDN)
- **Backend**: Render (supports FastAPI)
- **Best Performance**: Global CDN + optimized edge network

### Option 2: Both on Render
- **Frontend**: Render Static Site
- **Backend**: Render Web Service
- **Simpler Setup**: Single platform

---

## 📘 Quick Deployment Guide

### Vercel + Render (Recommended)

**1. Deploy Backend to Render:**
- Create Web Service with `backend` directory
- Add `HF_TOKEN` environment variable
- Build: `pip install -r requirements.txt && python init_vector_store.py`
- Start: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

**2. Deploy Frontend to Vercel:**
- Import repository to Vercel
- Set root directory to `frontend`
- Add environment variable: `VITE_API_URL` = your Render backend URL

**3. Update CORS:**
- Add Vercel URL to backend's `CORS_ORIGINS` environment variable

### 📖 Detailed Instructions

See **[DEPLOYMENT.md](./DEPLOYMENT.md)** for complete step-by-step guide including:
- Environment variable setup
- Troubleshooting tips
- Custom domain configuration
- Monitoring and logs

---

## 💰 Free Tier Limits

| Platform | Cost | Limits |
|----------|------|--------|
| **Vercel** | Free | 100GB bandwidth, unlimited requests |
| **Render** | Free | 750 hours/month, spins down after 15min inactivity |
| **HuggingFace** | Free | Rate limited (generous for personal use) |

Perfect for demos, portfolios, and personal projects!

---

## 📖 Usage

### Ask Questions

Simply type questions like:

```
"Who was Johann Sebastian Bach?"
"Tell me about Mozart's compositions"
"What period did Beethoven compose in?"
"Who were the major Romantic composers?"
```

The AI will:
1. Search the 107 composer biographies for relevant information
2. Generate an accurate answer using that context
3. Show you which composers' biographies were referenced

### Manage Conversations

- **New Chat**: Click "New Chat" in sidebar
- **Rename**: Click edit icon (✏️) next to session title
- **Delete Session**: Hover over conversation → trash icon
- **Delete Message**: Hover over message → trash icon

---

## 🏗️ Architecture

```
┌─────────────────┐      ┌──────────────┐      ┌─────────────────┐
│  React Frontend │ ───► │ FastAPI      │ ───► │  HuggingFace    │
│  (TypeScript)   │ HTTP │ Backend      │ API  │  Inference API  │
└─────────────────┘      └──────────────┘      └─────────────────┘
                                │
                                ▼
                         ┌──────────────┐
                         │  ChromaDB    │
                         │ (Vector DB)  │
                         │ 5,810 chunks │
                         └──────────────┘
```

### Tech Stack

**Frontend:**
- React 19 + TypeScript
- Vite build tool
- TailwindCSS
- Zustand (state management)
- React Query (data fetching)

**Backend:**
- FastAPI 0.127 (Python async framework)
- SQLAlchemy 2.0 (ORM)
- LangChain 1.2 (LLM orchestration)
- ChromaDB (vector database)
- Pydantic 2.12 (validation)

**AI/ML:**
- HuggingFace Inference API
- Llama 3.2-3B-Instruct (chat model)
- sentence-transformers (embeddings)

---

## 📁 Project Structure

```
classical-music-qa/
├── backend/
│   ├── app/
│   │   ├── models/              # Database models
│   │   │   ├── session.py       # Chat sessions
│   │   │   ├── message.py       # Messages
│   │   │   ├── document.py      # Documents
│   │   │   └── composer.py      # Composers
│   │   ├── routers/             # API routes
│   │   │   ├── chat.py          # Chat endpoints
│   │   │   ├── sessions.py      # Session management
│   │   │   └── documents.py     # Document upload
│   │   ├── services/            # Business logic
│   │   │   ├── chat_service.py      # Chat handling
│   │   │   ├── vector_service.py    # RAG/embeddings
│   │   │   └── document_service.py  # Doc processing
│   │   ├── scrapers/            # Web scrapers
│   │   │   ├── wikipedia_scraper.py
│   │   │   ├── imslp_scraper.py
│   │   │   └── allmusic_scraper.py
│   │   ├── config.py            # Configuration
│   │   └── main.py              # FastAPI app
│   ├── data/
│   │   ├── composer_sources/    # 107 composer biographies
│   │   │   ├── Baroque/
│   │   │   ├── Classical/
│   │   │   ├── Romantic/
│   │   │   └── ...
│   │   ├── documents/           # Uploaded files
│   │   ├── chroma_db/           # Vector store
│   │   └── chat.db              # SQLite DB
│   ├── init_vector_store.py     # Startup initialization
│   ├── run.py                   # Dev server
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── chat/            # Chat interface
│   │   │   ├── sessions/        # Sidebar
│   │   │   └── documents/       # Doc upload
│   │   ├── services/            # API clients
│   │   ├── stores/              # State management
│   │   └── App.tsx
│   ├── package.json
│   └── .env.example
│
├── render.yaml                  # Render deployment config
└── README.md
```

---

## 🎼 Composer Knowledge Base

The app includes comprehensive biographies of 107 composers:

**Medieval** (2): Hildegard von Bingen, Guillaume de Machaut
**Renaissance** (7): Josquin, Palestrina, Byrd, Tallis, Monteverdi, and more
**Baroque** (12): Bach, Handel, Vivaldi, Purcell, Rameau, and more
**Classical** (8): Mozart, Beethoven, Haydn, Schubert, and more
**Romantic** (37): Brahms, Chopin, Wagner, Verdi, Tchaikovsky, and more
**20th Century** (28): Debussy, Stravinsky, Bartók, Prokofiev, and more
**Contemporary** (13): Glass, Reich, Pärt, Adams, and more

Total: **5,810 text chunks** embedded and searchable

---

## 🔌 API Endpoints

### Chat

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/chat/message` | Send message, get AI response |
| GET | `/api/chat/history/{session_id}` | Get chat history |
| DELETE | `/api/chat/message/{message_id}` | Delete message |

### Sessions

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/sessions` | Create new session |
| GET | `/api/sessions` | List all sessions |
| PATCH | `/api/sessions/{session_id}` | Update title |
| DELETE | `/api/sessions/{session_id}` | Delete session |

### Documents

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/documents/upload` | Upload document |
| GET | `/api/documents` | List documents |
| DELETE | `/api/documents/{doc_id}` | Delete document |

---

## ⚙️ Configuration

### Environment Variables

**Backend** (`.env`):
```bash
# HuggingFace API Token (required)
HF_TOKEN=hf_your_token_here

# Model Configuration
DEFAULT_MODEL=meta-llama/Llama-3.2-3B-Instruct
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

# Database
DATABASE_URL=sqlite:///./data/chat.db

# Application
DEBUG=false

# CORS (comma-separated)
CORS_ORIGINS=https://your-frontend-url.onrender.com
```

**Frontend** (`.env`):
```bash
# Backend API URL
VITE_API_URL=https://your-backend-url.onrender.com
```

---

## 🐛 Troubleshooting

### Backend won't start
```bash
# Check HF_TOKEN is set
cat backend/.env

# Check dependencies
cd backend
pip install -r requirements.txt
```

### Frontend shows CORS error
- Verify `CORS_ORIGINS` in backend includes your frontend URL
- Restart backend after changing environment variables

### Chat returns empty responses
- Verify HF_TOKEN is valid
- Check backend logs for API errors
- Ensure vector store initialized (5,810 chunks)

### Slow first response on Render
- Free tier spins down after 15 minutes
- First request has 30-60 second cold start
- Subsequent requests are fast

---

## 💰 Cost

**100% FREE** when deployed to:
- Render Free Tier (750 hours/month)
- HuggingFace Inference API (free tier, rate limited)

Perfect for demos, learning, and personal projects!

---

## 🗺️ Roadmap

- [x] 107 composer biographies
- [x] RAG-powered chat
- [x] Session management
- [x] HuggingFace deployment
- [x] Render deployment config
- [ ] Export conversations
- [ ] Additional composers
- [ ] Multi-language support
- [ ] Audio examples integration

---

## 📄 License

MIT License - See LICENSE file for details

---

## 🙏 Credits

Built with:
- [HuggingFace](https://huggingface.co/) - Free LLM inference
- [FastAPI](https://fastapi.tiangolo.com/) - Python web framework
- [LangChain](https://langchain.com/) - LLM orchestration
- [ChromaDB](https://www.trychroma.com/) - Vector database
- [React](https://reactjs.org/) - UI framework
- [Render](https://render.com/) - Free hosting

Data sources: Wikipedia, IMSLP, AllMusic

---

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

---

**Enjoy exploring classical music with AI! 🎵**
