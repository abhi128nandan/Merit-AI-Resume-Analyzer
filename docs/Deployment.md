# 🚀 Production Deployment Guide

## Overview

This guide details deploying Merit AI to production using **Vercel** (Frontend) and **Render / Railway / Docker** (Backend).

---

## 1. Containerized Deployment (Docker & Docker Compose)

The repository provides production-ready deployment setups for full-stack dockerization.

### Single-Command Local Production Stack
```bash
docker-compose up --build -d
```
- Frontend available at `http://localhost:3000`
- Backend API available at `http://localhost:8000`

---

## 2. Deploying Backend API to Render / Railway

### Configuration
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4`

### Required Environment Variables
| Variable | Value Description | Example |
|---|---|---|
| `ENVIRONMENT` | Deployment environment | `production` |
| `GROQ_API_KEY` | API Key for Groq LLaMA models | `gsk_...` |
| `GEMINI_API_KEY` | API Key for Google Gemini models | `AIza...` |
| `CORS_ORIGINS` | Allowed Frontend Domain(s) | `https://merit-ai.vercel.app` |

---

## 3. Deploying Frontend to Vercel

1. Connect your GitHub repository to Vercel.
2. Set **Root Directory** to `frontend`.
3. Set **Framework Preset** to `Next.js`.
4. Add Environment Variable:
   ```env
   NEXT_PUBLIC_API_BASE_URL=https://your-backend-api.onrender.com
   ```
5. Click **Deploy**.
