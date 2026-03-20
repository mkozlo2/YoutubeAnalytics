# YouTube Partner Analytics + Optimization Platform

A recruiter-friendly full-stack platform for creators, media teams, and content partners to connect a YouTube account, sync performance data, inspect analytics dashboards, review underperforming videos, and troubleshoot OAuth/API issues.

## Highlights

- Google OAuth 2.0 flow scaffolding for YouTube private data access
- FastAPI backend with SQLAlchemy models and sync/debug endpoints
- React + TypeScript + Vite + Tailwind frontend with polished dashboards
- PostgreSQL-ready schema for channels, videos, metrics, recommendations, and sync logs
- Rule-based optimization engine with a path for LLM-generated summaries
- Demo mode so the app works immediately without live YouTube credentials

## Stack

- Frontend: React, TypeScript, Vite, Tailwind CSS, Recharts
- Backend: FastAPI, SQLAlchemy, Pydantic, HTTPX
- Database: PostgreSQL
- Auth: Google OAuth 2.0
- Jobs: APScheduler-ready service layer
- AI: OpenAI-ready recommendation summary hook

## Quick Start

### Docker

```bash
cp .env.example .env
docker compose up --build
```

Frontend: `http://localhost:5173`

Backend: `http://localhost:8000`

### Local Development

Backend:

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```

## OAuth Scopes

- `openid`
- `https://www.googleapis.com/auth/userinfo.email`
- `https://www.googleapis.com/auth/userinfo.profile`
- `https://www.googleapis.com/auth/youtube.readonly`
- `https://www.googleapis.com/auth/yt-analytics.readonly`

## Production Notes

- Set `DEMO_MODE=false` and configure Google OAuth credentials
- Replace local token encryption key with a secure secret manager value
- Add Alembic migrations before production deployment
- Prefer server-side sessions or signed cookies for authenticated frontend sessions
- Add background sync scheduling with APScheduler or Celery for periodic refresh

## Project Layout

```text
frontend/   React dashboard client
backend/    FastAPI API, services, SQLAlchemy models
docs/       Architecture, schema, API design, troubleshooting
```
