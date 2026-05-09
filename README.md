# 📰 German News Summarizer

An AI-powered application that extracts, analyzes, and summarizes German news articles. Get key insights, entity recognition, and automated translations in seconds.

## ✨ Features

- **Article Analysis** — Extract and analyze German news articles by URL or direct text input
- **Dual Language Summaries** — Automatic summaries in both German and English
- **Named Entity Recognition** — Identify people, organizations, and locations mentioned in articles
- **Keyword Extraction** — Automatically extract relevant keywords and topics
- **Tone Analysis** — Detect article sentiment and tone
- **Reading Time Estimation** — Quick overview of article length

## 🚀 Live Demo

[**Try the application**](https://german-news-summarizer.vercel.app) — Input any German news article and get instant analysis.

## 🏗️ Technology Stack

| Layer | Technologies |
|-------|--------------|
| **Frontend** | React, TypeScript, Vite, Tailwind CSS |
| **Backend** | FastAPI, Python |
| **NLP** | spaCy, Hugging Face Transformers, Language Detection |
| **Deployment** | Vercel (Frontend), Render/Railway/Fly (Backend) |

## 💡 How It Works

1. **Input** — Provide a German news article URL or paste text directly
2. **Processing** — The backend extracts content, detects language, and runs NLP analysis
3. **Output** — Receive structured analysis including summaries, entities, keywords, and tone

### Example API Response

```json
{
  "title": "Article Title",
  "source": "Der Spiegel",
  "language": "de",
  "reading_time_minutes": 4,
  "german_summary": "Concise German summary...",
  "english_summary": "Concise English summary...",
  "keywords": ["keyword1", "keyword2", "keyword3"],
  "entities": {
    "people": ["Person 1", "Person 2"],
    "organizations": ["Organization 1"],
    "locations": ["Berlin", "Munich"]
  },
  "tone": "neutral"
}
```

## 📊 Use Cases

- **Content Curation** — Quickly summarize multiple articles
- **Research** — Extract key information from German news sources
- **Language Learning** — Compare German and English versions side-by-side
- **News Monitoring** — Identify key entities and topics across articles
- **Content Analysis** — Understand article tone and structure

## 🎯 Project Goals

This is a full-stack AI portfolio project demonstrating:
- Modern web development practices (React, FastAPI)
- NLP and machine learning integration
- Full-stack deployment and DevOps
- Production-ready API design

## 📝 License

[Add your license here]

## 👤 About

Built as a portfolio project to showcase full-stack development and NLP capabilities.

For development setup and contribution guidelines, see [DEVELOPMENT.md](DEVELOPMENT.md).
