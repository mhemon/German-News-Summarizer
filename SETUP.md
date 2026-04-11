# German News Summarizer - Setup & Run Guide

## 📁 Project Structure Created

```
d:\German News Summarizer\
├── frontend/                    # React + Vite + TypeScript + Tailwind
│   ├── src/
│   │   ├── components/          # React components
│   │   │   ├── InputForm.tsx    # Article input form
│   │   │   └── ResultsCard.tsx  # Results display
│   │   ├── pages/               # Page components
│   │   ├── hooks/               # Custom React hooks
│   │   ├── lib/                 # API client
│   │   │   └── api.ts           # API call functions
│   │   ├── types/               # TypeScript types
│   │   │   └── api.ts           # API schemas
│   │   ├── App.tsx              # Main app component
│   │   ├── main.tsx             # React entry point
│   │   └── index.css            # Tailwind styles
│   ├── index.html               # HTML template
│   ├── package.json             # Dependencies
│   ├── vite.config.ts           # Vite config
│   ├── tsconfig.json            # TypeScript config
│   ├── tailwind.config.js       # Tailwind config
│   ├── postcss.config.js        # PostCSS config
│   └── .gitignore
│
├── backend/                     # FastAPI + Python
│   ├── app/
│   │   ├── api/                 # API routes
│   │   │   └── routes.py        # FastAPI endpoints
│   │   ├── services/            # Business logic
│   │   │   └── analyzer.py      # Article analysis service
│   │   ├── models/              # Data schemas
│   │   │   └── schemas.py       # Pydantic models
│   │   ├── core/                # Core config
│   │   │   └── config.py        # Settings
│   │   ├── utils/               # Utilities
│   │   │   └── helpers.py       # Helper functions
│   │   └── main.py              # FastAPI app entry
│   ├── requirements.txt         # Python dependencies
│   ├── .env.example             # Environment variables template
│   └── .gitignore
│
└── README.md                    # Project README
```

## 🚀 Quick Start (5 minutes)

### Step 1: Backend Setup

Open **Terminal 1** and run:

```powershell
cd "d:\German News Summarizer\backend"

# Create virtual environment
python -m venv venv

# Install dependencies using the venv Python directly
.\venv\Scripts\python.exe -m pip install --upgrade pip setuptools wheel
.\venv\Scripts\python.exe -m pip install --only-binary=:all: -r requirements.txt

# Run server
.\venv\Scripts\python.exe -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

✅ You should see: `Uvicorn running on http://127.0.0.1:8000`

Visit http://localhost:8000/docs to see interactive API documentation.


### Step 2: Frontend Setup

Open **Terminal 2** and run:

```powershell
cd "d:\German News Summarizer\frontend"

# Install dependencies
npm.cmd install

# Run dev server
npm.cmd run dev
```

✅ You should see: `Local: http://localhost:5173/`

## ✅ Test the Connection

1. Open browser to http://localhost:5173
2. You should see the German News Summarizer app
3. The header should show ✅ status (backend connected)
4. Try the "Load Example" button
5. Click "Analyze Article"
6. You should see mock results with German and English summaries

## 🧪 Test API Directly

### Get Health Status
```bash
curl http://localhost:8000/api/health
```

Expected response:
```json
{"status":"ok"}
```

### Analyze Article
```bash
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "input": "Pasted article text or URL here",
    "mode": "auto",
    "summary_length": "medium"
  }'
```

## 📋 Files Created

### Frontend (React + TypeScript + Vite)
- ✅ React app with modern setup
- ✅ TypeScript for type safety
- ✅ Tailwind CSS for styling
- ✅ API integration ready
- ✅ Structured components and services
- ✅ Type-safe API requests

### Backend (FastAPI + Python)
- ✅ FastAPI with CORS enabled
- ✅ Mock `/analyze` endpoint ready
- ✅ Mock `/health` endpoint
- ✅ Pydantic schemas for validation
- ✅ Modular service architecture
- ✅ Configuration management
- ✅ Helper utilities

## 🔌 How They Connect

Frontend Vite dev server (`localhost:5173`) proxies API calls to Backend (`localhost:8000`):

```
Browser Request → Vite (5173) → Proxy → FastAPI (8000) → Response
```

This is configured in [vite.config.ts](vite.config.ts#L11-L17).

## 📝 Current State

This scaffold includes:

1. **Mock Endpoint Working** - API returns realistic mock data
2. **Frontend Form** - Input accepts URL or text
3. **Results Display** - Cards for summaries, keywords, entities
4. **Loading States** - Spinner while processing
5. **Error Handling** - Clear error messages
6. **Responsive Design** - Works on mobile and desktop
7. **Type Safety** - Full TypeScript + Pydantic support

## 🎯 Next Phase Tasks

Once this scaffold is running, next implement:

1. **Phase 3:** Real article extraction (trafilatura)
2. **Phase 4:** German/English summarization 
3. **Phase 5:** NER, keywords, tone detection
4. **Phase 6:** UI polish and copy buttons
5. **Phase 7:** Deployment setup

## 🐛 Troubleshooting

### Backend won't start
- Check Python version: `python --version` (need 3.8+)
- If `python` is not recognized, install Python and reopen terminal (for Windows: `winget install -e --id Python.Python.3.12`)
- Verify the venv exists: `Test-Path .\venv\Scripts\python.exe`
- Reinstall with wheel-only mode:
  ` .\venv\Scripts\python.exe -m pip install --only-binary=:all: -r requirements.txt `
- If pydantic-core still fails on Python 3.13, use Python 3.12 for this project.

### Frontend shows connection error
- Ensure backend is running on port 8000
- Check browser console (F12) for error details
- Verify proxy is working: check Network tab

### npm is blocked in PowerShell
- Use `npm.cmd` instead of `npm` in PowerShell:
  `npm.cmd install`
  `npm.cmd run dev`
- Optional (current shell only): `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`

### Port already in use
- Change port in backend: `--port 8001`
- Change port in frontend: edit `vite.config.ts`

## ✨ What's Included

- ✅ Full TypeScript support
- ✅ Modern React (18.2.0) with hooks
- ✅ Tailwind CSS styling
- ✅ FastAPI with async support
- ✅ Pydantic for data validation
- ✅ CORS ready for deployment
- ✅ Professional folder structure
- ✅ Mock data for testing
- ✅ Error handling throughout
- ✅ Ready for real NLP integration

## 🚢 Next: Integration Tasks

After confirming mock version works:
- Replace `AnalysisService` with real NLP
- Integrate trafilatura for URL extraction
- Add transformation models for summarization
- Connect translation API
- Add spaCy for NER

---

**Questions?** Check the API docs at http://localhost:8000/docs (interactive Swagger UI)
