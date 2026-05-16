# ⬡ Agent Guti — AI Research Assistant

A full-stack AI research agent that helps find academic papers, search the web, and answer questions in Bengali, English, or Banglish.

🔗 **Live Demo:** [chimerical-stroopwafel-5b91f3.netlify.app](https://chimerical-stroopwafel-5b91f3.netlify.app)

---

## Features

- 📄 **Research Paper Search** — Find papers by topic, title, DOI, or abstract snippet (arXiv, Semantic Scholar, Papers With Code)
- 🌐 **Web Search** — Real-time web search via Tavily API
- 🤖 **Multi-Model Support** — Switch between multiple free LLMs with live status indicators (green/red dot)
- 🔐 **Auth System** — Login/Register via Supabase (per-user chat history)
- 💬 **Chat History** — Session titles saved per user, persistent across sessions
- 🌙 **Dark/Light Mode** — Toggle theme
- ⏹ **Pause Response** — Stop streaming mid-response
- 📏 **Resizable Sidebar** — Drag to resize
- 🇧🇩 **Multilingual** — Responds in Bengali, English, or Banglish based on input

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | FastAPI, Python |
| Agent Framework | LangGraph, LangChain |
| LLMs | OpenRouter (GPT-OSS 120B, DeepSeek V4 Flash, Gemma 4, MiniMax, etc.) |
| Web Search | Tavily API |
| Auth & DB | Supabase (PostgreSQL) |
| Frontend | Vanilla HTML/CSS/JS |
| Backend Deploy | Railway (aman11-id)|
| Frontend Deploy | Netlify (aman11-id)|

---

## Project Structure

```
Agent-Guti/
├── backend/
│   ├── main.py          # FastAPI app
│   └── requirements.txt
├── frontend/
│   └── index.html       # Single-page UI
├── test_models.py       # Model availability tester
├── .gitignore
└── README.md
```

---

## Setup Locally

### 1. Clone the repo

```bash
git clone https://github.com/AMANOT-ULLAH/Agent-Guti-.git
cd Agent-Guti-
```

### 2. Create `.env` file in root

```env
OPENROUTER_API_KEY=your_openrouter_key
TAVILY_API_KEY=your_tavily_key
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your_supabase_anon_key
```

### 3. Install dependencies & run backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### 4. Run frontend

```bash
cd frontend
python3 -m http.server 3000
# Open http://localhost:3000
```

---

## Supabase Setup

Run this SQL in Supabase SQL Editor:

```sql
-- Chat logs
create table if not exists chat_logs (
  id uuid default gen_random_uuid() primary key,
  user_id uuid,
  session_id text,
  model text,
  message text,
  response text,
  created_at timestamptz default now()
);

-- Chat history titles
create table if not exists chat_history (
  id uuid default gen_random_uuid() primary key,
  user_id uuid not null,
  session_id text not null unique,
  title text,
  updated_at timestamptz default now()
);
```

---

## Available Free Models

| Model | Description |
|-------|-------------|
| Auto | OpenRouter auto-selects best available |
| GPT-OSS 120B | Most reliable (OpenAI open weights) |
| GPT-OSS 20B | Lightweight, fast |
| Nemotron Nano 12B | Fastest response |
| DeepSeek V4 Flash | 1M context window |
| Gemma 4 31B | Google, multimodal capable |
| MiniMax M2.5 | Strong general model |
| Owl Alpha | Agentic tasks |

---

## Deploy

### Backend → Railway
1. Connect GitHub repo
2. Set root directory: `backend`
3. Add environment variables
4. Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

### Frontend → Netlify
1. Connect GitHub repo
2. Set publish directory: `frontend`
3. Deploy

---

## Known Issues

- Some free models hit rate limits frequently — switch to another model when red dot appears
- Chat history requires login — guest users don't get persistent history
- Pause button may not work instantly on slow responses

---

## License

MIT License — free to use, modify, and distribute.

---

*Built by [AMANOT-ULLAH](https://github.com/AMANOT-ULLAH)*
