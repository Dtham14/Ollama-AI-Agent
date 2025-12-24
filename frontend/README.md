# Music Theory Q&A Frontend

React + TypeScript frontend for the Music Theory Q&A application.

## Features

- 💬 Real-time chat interface with markdown support
- 📚 Source citations showing which documents were used
- 🗂️ Session management with history
- 🎨 Modern UI with Tailwind CSS
- ⚡ Fast development with Vite
- 🔄 State management with Zustand

## Tech Stack

- **React 18** - UI library
- **TypeScript** - Type safety
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **Zustand** - State management
- **Axios** - API client
- **React Markdown** - Markdown rendering
- **Lucide React** - Icons

## Getting Started

### Prerequisites

- Node.js 18+
- Backend API running on http://localhost:8000

### Installation

1. Install dependencies:
   ```bash
   npm install
   ```

2. Create environment file:
   ```bash
   cp .env.example .env
   ```

3. Start development server:
   ```bash
   npm run dev
   ```

   The app will be available at `http://localhost:5173`

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Lint code

## Project Structure

```
src/
├── components/          # React components
│   ├── chat/           # Chat interface components
│   └── sessions/       # Session sidebar
├── services/           # API clients
├── stores/             # Zustand state stores
├── types/              # TypeScript types
├── utils/              # Utility functions
├── App.tsx             # Root component
└── main.tsx            # Entry point
```

## Usage

1. Start a new chat by clicking "New Chat"
2. Type your question about music theory
3. View the AI response with source citations
4. Access previous conversations from the sidebar

## Development

The frontend communicates with the FastAPI backend at `http://localhost:8000`. Make sure the backend is running before starting the frontend.

## Building for Production

```bash
npm run build
```

The built files will be in the `dist/` directory.
