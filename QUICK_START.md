# Quick Start Guide

Get your Music Theory Q&A application running in 3 steps!

## Prerequisites

- Python 3.10+
- Node.js 18+
- Ollama installed with models: `llama3.2` and `mxbai-embed-large`

## Step 1: Start the Backend

```bash
# Navigate to backend directory
cd backend

# Start the FastAPI server
../.venv/Scripts/python.exe run.py
```

The backend API will be available at `http://localhost:8000`
- API docs: `http://localhost:8000/docs`
- Health check: `http://localhost:8000/health`

## Step 2: Start the Frontend

In a new terminal:

```bash
# Navigate to frontend directory
cd frontend

# Start the Vite dev server
npm run dev
```

The frontend will be available at `http://localhost:5173`

## Step 3: Start Chatting!

1. Open `http://localhost:5173` in your browser
2. Click "New Chat" to start a conversation
3. Ask questions about music theory!

## Example Questions

Try asking:
- "What forms did Chopin use in his waltzes?"
- "How did Chopin use rubato in his performances?"
- "Explain Chopin's use of chromatic harmony"
- "What is unique about mazurka rhythm?"
- "Tell me about Chopin's use of pedaling"

## Troubleshooting

### Backend won't start
- Make sure Ollama is running: `ollama list`
- Check that both models are installed:
  - `ollama pull llama3.2`
  - `ollama pull mxbai-embed-large`
- Verify virtual environment: `../.venv/Scripts/python.exe --version`

### Frontend won't connect to backend
- Ensure backend is running on port 8000
- Check `.env` file in frontend folder has `VITE_API_URL=http://localhost:8000`
- Clear browser cache and reload

### No responses from AI
- Check Ollama service is running
- Look at backend logs for errors
- Verify models are loaded: `ollama list`

## Next Steps

- **Add documents**: Implement Phase 3 document upload feature
- **Fine-tune models**: Create custom music theory models
- **Deploy**: Use Docker for production deployment

## Architecture

```
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│   React     │ ───> │   FastAPI   │ ───> │   Ollama    │
│  Frontend   │ HTTP │   Backend   │      │     LLM     │
│  :5173      │ <─── │   :8000     │ <─── │  :11434     │
└─────────────┘      └──────┬──────┘      └─────────────┘
                            │
                            ├─> SQLite (Chat History)
                            └─> Chroma DB (Vector Store)
```

## Support

- View API docs: `http://localhost:8000/docs`
- Check logs in terminal windows
- Review README files in `backend/` and `frontend/`

Enjoy exploring music theory with AI! 🎵
