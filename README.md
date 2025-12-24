# 🎵 Music Theory Q&A - AI-Powered Learning Assistant

A full-stack web application that combines **Ollama LLMs** with **RAG (Retrieval Augmented Generation)** to create an intelligent music theory learning assistant. Built with FastAPI, React, and ChromaDB for local, private AI conversations.

[![FastAPI](https://img.shields.io/badge/FastAPI-0.127.0-009688?logo=fastapi)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-19.2.0-61DAFB?logo=react)](https://reactjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.9.3-3178C6?logo=typescript)](https://www.typescriptlang.org/)
[![Ollama](https://img.shields.io/badge/Ollama-llama3.2-000000?logo=llama)](https://ollama.ai/)

---

## ✨ Features

### 💬 **Interactive Chat**
- Real-time conversations with AI about music theory
- Context-aware responses using RAG
- Source citations showing which documents informed each answer
- Persistent chat history across sessions

### 📚 **Document Management**
- **UI Upload**: Drag-and-drop PDF, DOCX, TXT, MD, CSV files
- **Bulk Training**: Place PDFs in a folder and process them all at once
- Automatic text extraction and chunking
- Vector embeddings with `mxbai-embed-large`
- ChromaDB for fast semantic search

### 🗂️ **Session Management**
- Create, rename, and delete conversations
- View conversation history
- Switch between multiple sessions
- Automatic session tracking

### ✏️ **Message Control**
- Delete individual messages
- Edit conversation context
- Clear entire sessions

### 🎯 **Smart Features**
- Source attribution with relevance scores
- Automatic document deduplication
- Model selection (currently llama3.2)
- Fully local - no data sent to cloud

---

## 🚀 Quick Start

### Prerequisites

1. **Ollama** - [Install Ollama](https://ollama.com/download)
2. **Python 3.10+** - For backend
3. **Node.js 18+** - For frontend

### Install Ollama Models

```bash
ollama pull llama3.2
ollama pull mxbai-embed-large
```

### Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the server
python run.py
```

Backend runs at: `http://localhost:8000`
API docs at: `http://localhost:8000/docs`

### Frontend Setup

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

## 📖 Usage Guide

### Training the AI

#### Method 1: UI Upload (Best for individual documents)

1. Open the app at `http://localhost:5173`
2. Navigate to **Documents** section
3. Drag and drop PDF files or click to browse
4. Files are automatically processed and embedded

#### Method 2: Bulk Folder Training (Best for many documents)

```bash
# 1. Place your PDFs in the training folder
cp your-music-theory-pdfs/*.pdf backend/data/training_docs/

# 2. Run the training script
cd backend
python train_from_folder.py

# To force reprocess all files:
python train_from_folder.py --force
```

**Output Example:**
```
============================================================
Music Theory Knowledge Base - Bulk Training Tool
============================================================

Training folder: backend/data/training_docs

Found 5 documents to process

Processing: music-fundamentals.pdf
   [SUCCESS] Processed! (42 chunks)
Processing: harmony-basics.pdf
   [SUCCESS] Processed! (35 chunks)
[SKIP] Already processed: scales-guide.pdf

============================================================
Summary:
   Processed: 2
   Skipped: 3
   Errors: 0
   Total: 5
============================================================
```

### Managing Conversations

**Create a new chat:**
- Click "New Chat" button in sidebar

**Rename a conversation:**
- Hover over conversation → Click edit icon (pencil)
- Type new name → Press Enter

**Delete a conversation:**
- Hover over conversation → Click trash icon
- Confirm deletion

**Delete a message:**
- Hover over any message → Click trash icon
- Confirm deletion

### Asking Questions

Simply type your question in the chat:

```
"What is a perfect fifth interval?"
"Explain the circle of fifths"
"What are the notes in a C major scale?"
```

The AI will:
1. Search your uploaded documents for relevant content
2. Generate an answer using that context
3. Show you which documents were used (with relevance scores)

---

## 🏗️ Architecture

```
┌─────────────────┐      ┌──────────────┐      ┌─────────────┐
│  React Frontend │ ───► │ FastAPI      │ ───► │   Ollama    │
│  (TypeScript)   │ HTTP │ Backend      │ gRPC │  (llama3.2) │
└─────────────────┘      └──────────────┘      └─────────────┘
                                │
                                ▼
                         ┌──────────────┐
                         │  ChromaDB    │
                         │ (Vector DB)  │
                         └──────────────┘
```

### Tech Stack

**Frontend:**
- React 19.2 + TypeScript
- Vite for build tooling
- TailwindCSS for styling
- Zustand for state management
- React Query for data fetching
- Axios for HTTP requests

**Backend:**
- FastAPI 0.127 (async Python web framework)
- SQLAlchemy 2.0 (ORM)
- LangChain 1.2 (LLM orchestration)
- ChromaDB 1.4 (vector database)
- Pydantic 2.12 (data validation)

**AI/ML:**
- Ollama (local LLM runtime)
- llama3.2 (language model)
- mxbai-embed-large (embedding model)

---

## 📁 Project Structure

```
Ollama-AI-Agent/
├── backend/
│   ├── app/
│   │   ├── models/              # SQLAlchemy models
│   │   │   ├── session.py       # Chat sessions
│   │   │   ├── message.py       # Chat messages
│   │   │   └── document.py      # Uploaded documents
│   │   ├── routers/             # API endpoints
│   │   │   ├── chat.py          # Chat & messages
│   │   │   ├── sessions.py      # Session management
│   │   │   ├── documents.py     # Document upload
│   │   │   └── models.py        # LLM model info
│   │   ├── services/            # Business logic
│   │   │   ├── chat_service.py      # Chat handling
│   │   │   ├── document_service.py  # Doc processing
│   │   │   └── vector_service.py    # Embeddings
│   │   ├── schemas/             # Pydantic schemas
│   │   ├── config.py            # Configuration
│   │   ├── database.py          # DB connection
│   │   └── main.py              # FastAPI app
│   ├── data/
│   │   ├── documents/           # Uploaded files
│   │   ├── training_docs/       # Bulk training folder
│   │   ├── chroma_db/           # Vector database
│   │   └── chat.db              # SQLite database
│   ├── train_from_folder.py     # Bulk training script
│   ├── run.py                   # Server entry point
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── chat/            # Chat UI
│   │   │   ├── sessions/        # Sidebar
│   │   │   └── documents/       # Doc upload
│   │   ├── services/            # API clients
│   │   ├── stores/              # State management
│   │   ├── types/               # TypeScript types
│   │   └── App.tsx
│   ├── package.json
│   └── vite.config.ts
│
├── NEW_FEATURES.md              # Feature documentation
└── README.md                    # This file
```

---

## 🔌 API Endpoints

### Chat

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/chat/message` | Send a message and get AI response |
| GET | `/api/chat/history/{session_id}` | Get chat history for session |
| DELETE | `/api/chat/history/{session_id}` | Delete entire session |
| DELETE | `/api/chat/message/{message_id}` | Delete individual message |

### Sessions

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/sessions` | Create new session |
| GET | `/api/sessions` | List all sessions |
| GET | `/api/sessions/{session_id}` | Get session details |
| PATCH | `/api/sessions/{session_id}` | Update session title |
| DELETE | `/api/sessions/{session_id}` | Delete session |

### Documents

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/documents/upload` | Upload and process document |
| GET | `/api/documents` | List all documents |
| GET | `/api/documents/{doc_id}` | Get document details |
| DELETE | `/api/documents/{doc_id}` | Delete document |
| POST | `/api/documents/{doc_id}/reembed` | Reprocess document |

### Models

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/models` | List available Ollama models |
| GET | `/api/models/current` | Get current model info |

---

## ⚙️ Configuration

Edit `backend/app/config.py` or create a `.env` file:

```python
# Application
APP_NAME = "Music Theory Q&A"
DEBUG = True

# Database
DATABASE_URL = "sqlite:///./data/chat.db"

# Ollama
OLLAMA_BASE_URL = "http://localhost:11434"
DEFAULT_MODEL = "llama3.2"
EMBEDDING_MODEL = "mxbai-embed-large"

# Vector Store
CHROMA_PERSIST_DIR = "./data/chroma_db"
CHROMA_COLLECTION_NAME = "music-theory-knowledge"

# Documents
UPLOAD_DIR = "./data/documents"
MAX_UPLOAD_SIZE = 10485760  # 10MB
ALLOWED_EXTENSIONS = {".pdf", ".txt", ".csv", ".docx", ".md"}

# RAG
RETRIEVAL_K = 3  # Number of documents to retrieve
```

---

## 🧪 Testing

### Test Message Deletion
```bash
# Create a test message
curl -X POST http://localhost:8000/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{"message":"Test question","include_sources":false}'

# Delete the message (use ID from response)
curl -X DELETE http://localhost:8000/api/chat/message/{message_id}
```

### Test Document Training
```bash
# Create test document
echo "Music theory test content" > backend/data/training_docs/test.txt

# Run training
cd backend
python train_from_folder.py
```

### Test Session Management
```bash
# List sessions
curl http://localhost:8000/api/sessions

# Rename a session
curl -X PATCH http://localhost:8000/api/sessions/{session_id} \
  -H "Content-Type: application/json" \
  -d '{"title":"My Music Theory Session"}'
```

---

## 🐛 Troubleshooting

### Ollama not responding
```bash
# Check if Ollama is running
ollama list

# If not running, start it
ollama serve
```

### Backend errors
```bash
# Check logs in terminal
# Restart backend
cd backend
python run.py
```

### Frontend not updating
```bash
# Clear cache and restart
cd frontend
rm -rf node_modules/.vite
npm run dev
```

### Database issues
```bash
# Reset database (WARNING: Deletes all data)
rm backend/data/chat.db
rm -rf backend/data/chroma_db
```

---

## 📝 Development

### Running Tests
```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

### Code Style
```bash
# Backend (Python)
cd backend
black .
flake8 .

# Frontend (TypeScript)
cd frontend
npm run lint
```

---

## 🗺️ Roadmap

- [x] Chat interface with RAG
- [x] Document upload and processing
- [x] Session management
- [x] Message deletion
- [x] Bulk folder training
- [x] Session renaming
- [ ] Multi-model support
- [ ] Advanced RAG strategies
- [ ] Export conversations
- [ ] Docker deployment
- [ ] User authentication
- [ ] API rate limiting

---

## 📄 License

MIT License - See LICENSE file for details

---

## 🙏 Credits

Built with love using:
- [Ollama](https://ollama.ai/) - Local LLM runtime
- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [LangChain](https://langchain.com/) - LLM orchestration
- [ChromaDB](https://www.trychroma.com/) - Vector database
- [React](https://reactjs.org/) - UI framework
- [Vite](https://vitejs.dev/) - Build tool

---

## 💡 Tips

1. **Start with small documents** to test the system
2. **Use descriptive titles** for conversations to stay organized
3. **Include sources** in responses to verify information
4. **Regularly backup** your `data/` folder
5. **Use folder training** for bulk imports of related documents

---

## 🤝 Contributing

Contributions welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📧 Contact

For questions or feedback, please open an issue on GitHub.

---

**Happy Learning! 🎵**
