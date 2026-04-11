# German News Summarizer

A full-stack AI portfolio project demonstrating NLP capabilities with German news summarization.

## Project Structure

```
german-news-summarizer/
├── frontend/                 # React + Vite + TypeScript + Tailwind
│   ├── src/
│   ├── package.json
│   ├── vite.config.ts
│   └── index.html
├── backend/                  # FastAPI + Python
│   ├── app/
│   ├── main.py
│   └── requirements.txt
└── README.md
```

## Quick Start

### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
.\venv\Scripts\python.exe -m pip install --upgrade pip setuptools wheel
.\venv\Scripts\python.exe -m pip install --only-binary=:all: -r requirements.txt
# On macOS/Linux:
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r requirements.txt

# Run server
# On Windows:
.\venv\Scripts\python.exe -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
# On macOS/Linux:
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Backend will be available at: http://localhost:8000

### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
# On Windows PowerShell:
npm.cmd install
# On macOS/Linux:
npm install

# Run development server
# On Windows PowerShell:
npm.cmd run dev
# On macOS/Linux:
npm run dev
```

Frontend will be available at: http://localhost:5173

## Deployment

### Frontend on Vercel

1. Push this repository to GitHub.
2. In Vercel, create a new project and set the root directory to `frontend`.
3. Use defaults:
  - Build command: `npm run build`
  - Output directory: `dist`
4. Add environment variable in Vercel:
  - `VITE_API_BASE_URL=https://YOUR_BACKEND_DOMAIN/api`
5. Deploy.

### Backend hosting (Render/Railway/Fly)

Vercel is ideal for the React frontend. Host FastAPI backend on a Python host such as Render.

Set backend environment variables:

- `CORS_ORIGINS=https://YOUR_VERCEL_APP.vercel.app,http://localhost:5173`
- `APP_URL=https://YOUR_VERCEL_APP.vercel.app`

Run command:

`uvicorn app.main:app --host 0.0.0.0 --port 8000`

After backend deployment, update Vercel `VITE_API_BASE_URL` to the backend URL and redeploy frontend.

### Testing the Connection

1. Start the backend (runs on port 8000)
2. Start the frontend (runs on port 5173)
3. The frontend will proxy API requests to `http://localhost:8000/api`
4. You should see a green connection status in the header
5. Enter an article URL or text and click "Analyze Article"

## API Endpoints

### `GET /api/health`
Health check endpoint.

**Response:**
```json
{
  "status": "ok"
}
```

### `POST /api/analyze`
Analyze an article and return summaries and NLP analysis.

**Request:**
```json
{
  "input": "https://example.com/article or article text",
  "mode": "auto",
  "summary_length": "medium"
}
```

**Response:**
```json
{
  "title": "Article Title",
  "source": "Der Spiegel",
  "language": "de",
  "article_text": "Extracted article content...",
  "reading_time_minutes": 4,
  "german_summary": "German summary...",
  "english_summary": "English summary...",
  "keywords": ["keyword1", "keyword2"],
  "entities": {
    "people": ["Person 1"],
    "organizations": ["Org 1"],
    "locations": ["Location 1"]
  },
  "tone": "neutral"
}
```

## Stack

- **Frontend:** React, Vite, TypeScript, Tailwind CSS
- **Backend:** FastAPI, Python
- **NLP:** (To be integrated) spaCy, Hugging Face Transformers, LLM APIs

## Next Steps

1. Integrate real article extraction (trafilatura)
2. Add language detection (langdetect)
3. Implement German/English summarization
4. Add NER and keyword extraction
5. Deploy to Hugging Face Spaces or similar
