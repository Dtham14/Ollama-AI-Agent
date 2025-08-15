# Ollama-AI-Agent

##  Purpose

**Ollama-AI-Agent** is a Python-based project designed to use the power of the **Ollama** local LLM framework—specifically using the **Llama 3.2** model—to create an AI agent that understands 
and interacts with music theory. By combining the Llama 3.2 model with a dedicated embedding model (`mxbai-embed-large`), this project enables advanced music-theoretical reasoning, semantic retrieval, and context-aware responses—all running entirely locally.

---

##  Prerequisites

- **Python 3.10 or higher** (ideally Python 3.11+ for best compatibility).
- **Git** to clone the repo.
- **Ollama CLI** installed and configured — follow [Ollama’s installation instructions](https://ollama.com/) depending on your OS (macOS, Linux, or Windows):contentReference[oaicite:1]{index=1}.
- At least **8 GB RAM**, preferably more if using larger model variants :contentReference[oaicite:2]{index=2}.

---

##  Setup Instructions

```bash
git clone https://github.com/Dtham14/Ollama-AI-Agent.git
cd Ollama-AI-Agent

python3 -m venv venv
source venv/bin/activate        # macOS/Linux
.\venv\Scripts\activate     # Windows PowerShell or CMD

pip install --upgrade pip
pip install -r requirements.txt
