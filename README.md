# 🎵 Classical Music Q&A - AI-Powered Assistant

A production-ready Next.js application that combines **HuggingFace LLMs** with **RAG (Retrieval Augmented Generation)** to create an intelligent classical music assistant. Pre-loaded with biographies of 107+ major composers from Medieval to Contemporary periods.

[![Next.js](https://img.shields.io/badge/Next.js-15-000000?logo=next.js)](https://nextjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0-3178C6?logo=typescript)](https://www.typescriptlang.org/)
[![HuggingFace](https://img.shields.io/badge/HuggingFace-Llama_3.2-FFD21E?logo=huggingface)](https://huggingface.co/)
[![Pinecone](https://img.shields.io/badge/Pinecone-Vector_DB-00D4FF)](https://www.pinecone.io/)
[![Vercel](https://img.shields.io/badge/Deployed_on-Vercel-000000?logo=vercel)](https://vercel.com/)

---

## ✨ Features

### 💬 **Intelligent Chat**
- Ask questions about classical composers, their lives, works, and contributions
- Context-aware responses using RAG from 107+ composer biographies
- Source citations showing which documents informed each answer
- Persistent chat history across sessions

### 📚 **Rich Knowledge Base**
- **Pre-loaded**: 107 composer biographies (5,194 vectors)
- **Periods Covered**: Medieval, Renaissance, Baroque, Classical, Romantic, 20th Century, Contemporary
- **Major Composers**: Bach, Mozart, Beethoven, Brahms, Stravinsky, and 102 more
- Scraped from Wikipedia, IMSLP, and AllMusic
- Automatically embedded and searchable via Pinecone

### 🗂️ **Session Management**
- Create, rename, and delete conversations
- Edit conversation titles inline
- Switch between multiple sessions
- Automatic session tracking in PostgreSQL
- Message deletion for conversation editing

### 🚀 **Production Deployment**
- Deployed on Vercel with edge optimization
- Neon PostgreSQL serverless database
- Pinecone cloud vector database
- 100% free HuggingFace Inference API
- No credit card required for development

---

## 🚀 Quick Start (Local Development)

### Prerequisites

1. **Node.js 18+**
2. **HuggingFace Account** (free) - [Sign up](https://huggingface.co/join)
3. **Pinecone Account** (free) - [Sign up](https://www.pinecone.io/)

### 1. Get API Tokens

**HuggingFace Token:**
1. Go to [https://huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
2. Click "New token"
3. Name it (e.g., "classical-music-app")
4. Select "Read" permission
5. Copy the token (starts with `hf_...`)

**Pinecone API Key:**
1. Go to [https://app.pinecone.io/](https://app.pinecone.io/)
2. Create a new project or use existing
3. Go to "API Keys" and copy your API key
4. Create an index named `classical-music` with dimension `384` (for sentence-transformers/all-MiniLM-L6-v2)

### 2. Next.js App Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd Ollama-AI-Agent/nextjs-app

# Install dependencies
npm install --legacy-peer-deps

# Create .env file
cat > .env << EOF
DATABASE_URL="file:./dev.db"
HF_TOKEN=hf_your_token_here
PINECONE_API_KEY=pcsk_your_api_key_here
PINECONE_INDEX_NAME=classical-music
DEFAULT_MODEL=meta-llama/Llama-3.2-3B-Instruct
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
EOF

# Initialize database
npx prisma generate
npx prisma db push

# Upload composer data to Pinecone (one-time setup)
npx tsx scripts/uploadComposerData.ts

# Start dev server
npm run dev
```

App runs at: `http://localhost:3000`

---

## 🌐 Deployment to Vercel (100% Free)

### Prerequisites
- GitHub account
- Vercel account (sign up at [vercel.com](https://vercel.com))
- Pinecone account with classical-music index created
- Neon account (or other serverless PostgreSQL provider)

### Step-by-Step Deployment

**1. Push to GitHub:**
```bash
git add .
git commit -m "Prepare for deployment"
git push origin main
```

**2. Deploy to Vercel:**
- Go to [vercel.com](https://vercel.com) and log in
- Click "Add New Project"
- Import your GitHub repository
- **Set Root Directory** to `nextjs-app`
- Click "Deploy"

**3. Add Database (Neon):**
- In your Vercel project dashboard, go to "Storage"
- Click "Create Database"
- Select **Neon - Serverless Postgres**
- Leave "Custom Prefix" blank
- Click "Create"
- This automatically adds `POSTGRES_PRISMA_URL` environment variable

**4. Add Environment Variables:**
In your Vercel project settings, add:
```bash
HF_TOKEN=hf_your_token_here
PINECONE_API_KEY=pcsk_your_api_key_here
PINECONE_INDEX_NAME=classical-music
DEFAULT_MODEL=meta-llama/Llama-3.2-3B-Instruct
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
```

**5. Upload Data to Pinecone:**
```bash
# From your local machine (one-time setup)
cd nextjs-app
npx tsx scripts/uploadComposerData.ts
```

**6. Redeploy:**
- Go to Vercel dashboard → Deployments
- Click "Redeploy" on latest deployment
- Database tables will be created automatically

That's it! Your app is now live on Vercel.

---

## 🏗️ Architecture

```
┌─────────────────┐      ┌──────────────┐      ┌─────────────────┐
│  Next.js 15     │ ───► │ HuggingFace  │ ───► │  Llama 3.2-3B   │
│  Frontend + API │ API  │ Inference    │      │  Chat Model     │
└─────────────────┘      └──────────────┘      └─────────────────┘
         │
         ├────────────► ┌──────────────┐
         │              │  Pinecone    │
         │              │ Vector DB    │
         │              │ 5,194 vectors│
         │              └──────────────┘
         │
         └────────────► ┌──────────────┐
                        │  Neon/       │
                        │  PostgreSQL  │
                        │  (Sessions)  │
                        └──────────────┘
```

### Tech Stack

**Framework:**
- Next.js 15 (App Router)
- TypeScript 5.0
- React 19
- TailwindCSS 3

**Database & Storage:**
- Prisma ORM 6.19.1
- Neon PostgreSQL (serverless)
- Pinecone (cloud vector database)

**AI/ML:**
- HuggingFace Inference API
- Llama 3.2-3B-Instruct (chat model)
- sentence-transformers/all-MiniLM-L6-v2 (embeddings)

**Deployment:**
- Vercel (Next.js hosting)
- Neon (PostgreSQL)
- Pinecone (vector storage)

---

## 📁 Project Structure

```
Ollama-AI-Agent/
├── nextjs-app/                    # Next.js application
│   ├── app/
│   │   ├── api/                   # API routes
│   │   │   ├── chat/
│   │   │   │   └── message/       # Chat endpoint
│   │   │   ├── sessions/          # Session management
│   │   │   └── documents/         # Document upload
│   │   ├── page.tsx               # Main chat interface
│   │   ├── layout.tsx             # Root layout
│   │   └── globals.css            # Global styles
│   ├── components/
│   │   ├── chat/                  # Chat components
│   │   ├── sessions/              # Session sidebar
│   │   └── ui/                    # Reusable UI components
│   ├── lib/
│   │   ├── prisma.ts              # Prisma client
│   │   ├── vectorSearch.ts        # Pinecone RAG logic
│   │   └── utils.ts               # Utilities
│   ├── prisma/
│   │   └── schema.prisma          # Database schema
│   ├── scripts/
│   │   └── uploadComposerData.ts  # Pinecone upload script
│   ├── vercel.json                # Vercel build config
│   ├── package.json
│   └── .env.example
│
├── backend/                       # Legacy backend (reference only)
│   └── data/
│       └── composer_sources/      # 107 composer biographies
│           ├── Baroque/
│           ├── Classical/
│           ├── Romantic/
│           └── ...
│
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

Total: **5,194 vectors** embedded in Pinecone

---

## 🔌 API Routes

### Chat

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/chat/message` | Send message, get AI response |
| DELETE | `/api/chat/message/[id]` | Delete message |

### Sessions

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/sessions` | List all sessions |
| POST | `/api/sessions` | Create new session |
| PATCH | `/api/sessions/[id]` | Update session title |
| DELETE | `/api/sessions/[id]` | Delete session |

### Documents

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/documents` | List documents |
| POST | `/api/documents` | Upload document |
| DELETE | `/api/documents/[id]` | Delete document |

---

## ⚙️ Configuration

### Environment Variables

**Production (Vercel):**
```bash
# HuggingFace API Token (required)
HF_TOKEN=hf_your_token_here

# Pinecone Configuration (required)
PINECONE_API_KEY=pcsk_your_key_here
PINECONE_INDEX_NAME=classical-music

# Model Configuration
DEFAULT_MODEL=meta-llama/Llama-3.2-3B-Instruct
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

# Database (automatically added by Neon integration)
POSTGRES_PRISMA_URL=postgresql://...
POSTGRES_URL=postgresql://...
POSTGRES_URL_NON_POOLING=postgresql://...
```

**Local Development:**
```bash
# Use SQLite for local development
DATABASE_URL="file:./dev.db"

# Same API keys as production
HF_TOKEN=hf_your_token_here
PINECONE_API_KEY=pcsk_your_key_here
PINECONE_INDEX_NAME=classical-music
DEFAULT_MODEL=meta-llama/Llama-3.2-3B-Instruct
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
```

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
1. Generate embeddings for your question
2. Search Pinecone for relevant composer biographies
3. Use retrieved context to generate accurate answer
4. Show you which composers' biographies were referenced

### Manage Conversations

- **New Chat**: Click "New Chat" in sidebar
- **Rename**: Click edit icon (✏️) next to session title
- **Delete Session**: Hover over conversation → trash icon
- **Delete Message**: Hover over message → trash icon

---

## 🐛 Troubleshooting

### Database tables not created
```bash
# Run Prisma migrations locally
cd nextjs-app
npx prisma db push

# For Vercel, tables are created automatically on first deploy
# Check build logs in Vercel dashboard
```

### Pinecone returns no results
```bash
# Verify data was uploaded
# Run upload script from local machine
cd nextjs-app
npx tsx scripts/uploadComposerData.ts

# Check Pinecone dashboard for vector count (should be ~5,194)
```

### Chat returns empty responses
- Verify `HF_TOKEN` is valid in environment variables
- Check Vercel function logs for API errors
- Ensure Pinecone index has vectors

### TypeScript build errors
```bash
# Regenerate Prisma client
npx prisma generate

# Clear Next.js cache
rm -rf .next
npm run build
```

---

## 💰 Cost Breakdown

| Service | Free Tier | Usage |
|---------|-----------|-------|
| **Vercel** | 100GB bandwidth, unlimited deployments | Hosting |
| **Neon PostgreSQL** | 3GB storage, 0.5GB RAM | Database |
| **Pinecone** | 1 free index, 100K vectors | Vector search |
| **HuggingFace** | Rate limited (generous) | LLM inference |

**Total Cost: $0/month** for personal projects!

---

## 🗺️ Roadmap

- [x] 107 composer biographies
- [x] RAG-powered chat with Pinecone
- [x] Session management
- [x] HuggingFace LLM integration
- [x] Next.js migration
- [x] Vercel deployment
- [x] PostgreSQL integration
- [ ] Export conversations to PDF
- [ ] Additional composers (expand to 200+)
- [ ] Multi-language support
- [ ] Audio examples integration
- [ ] Advanced search filters

---

## 📄 License

MIT License - See LICENSE file for details

---

## 🙏 Credits

Built with:
- [Next.js](https://nextjs.org/) - React framework
- [HuggingFace](https://huggingface.co/) - Free LLM inference
- [Pinecone](https://www.pinecone.io/) - Vector database
- [Prisma](https://www.prisma.io/) - Database ORM
- [Neon](https://neon.tech/) - Serverless PostgreSQL
- [Vercel](https://vercel.com/) - Deployment platform
- [TailwindCSS](https://tailwindcss.com/) - Styling

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
