# Ollama Music Theory Q&A - Web Application

A modern web application for querying music theory knowledge using Ollama LLMs with RAG (Retrieval Augmented Generation).

## Features

- 💬 **Interactive Chat Interface** - Real-time Q&A with music theory expert AI
- 📚 **Document Upload** - Add your own music theory documents (PDF, DOCX, TXT, CSV, MD)
- 🎯 **Source Citations** - See which documents were used to answer each question
- 🔄 **Model Selection** - Switch between different Ollama models
- 📝 **Session Management** - Maintain conversation history across sessions
- 🎼 **Fine-Tuning Support** - Create custom models trained on your data

## Architecture

```
Frontend (React + TypeScript)  →  Backend (FastAPI)  →  Ollama + Chroma DB
```

## Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+ (for frontend)
- [Ollama](https://ollama.ai) installed and running
- Ollama models: `llama3.2` and `mxbai-embed-large`

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Create environment file:**
   ```bash
   cp .env.example .env
   ```

4. **Migrate legacy data (optional):**
   ```bash
   python scripts/migrate_legacy_data.py
   ```

5. **Run the server:**
   ```bash
   python run.py
   ```

   The API will be available at `http://localhost:8000`
   API docs at `http://localhost:8000/docs`

### Frontend Setup (Coming Soon)

Frontend React application is under development in Phase 2.

## Project Structure

```
Ollama-AI-Agent/
├── backend/               # FastAPI backend
│   ├── app/
│   │   ├── models/       # Database models
│   │   ├── schemas/      # Pydantic schemas
│   │   ├── services/     # Business logic
│   │   ├── routers/      # API endpoints
│   │   └── main.py       # FastAPI app
│   ├── data/             # Data storage
│   ├── legacy/           # Original CLI files
│   └── requirements.txt
├── frontend/             # React frontend (Phase 2)
└── README.md
```

## API Endpoints

### Chat
- `POST /api/chat/message` - Send a message
- `GET /api/chat/history/{session_id}` - Get chat history
- `DELETE /api/chat/history/{session_id}` - Clear history

### Models
- `GET /api/models` - List available models
- `POST /api/models/select` - Select a model
- `GET /api/models/current` - Get current model

### Sessions
- `POST /api/sessions` - Create new session
- `GET /api/sessions` - List all sessions
- `GET /api/sessions/{session_id}` - Get session details

## Development Status

✅ **Phase 1 Complete:** Backend Foundation
- FastAPI server with REST API
- SQLAlchemy database models
- Chat service with LLM integration
- Vector store for RAG
- Session management

🚧 **Phase 2 In Progress:** Frontend Foundation
- React + TypeScript setup
- Chat UI components
- State management
- API integration

📋 **Planned:**
- Document upload feature
- Fine-tuning workflow
- Docker deployment
- Advanced RAG features

## License

MIT

## Credits

Built with:
- [FastAPI](https://fastapi.tiangolo.com/)
- [LangChain](https://langchain.com/)
- [Ollama](https://ollama.ai/)
- [Chroma](https://www.trychroma.com/)
