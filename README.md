# 🤖 AI Job Search Assistant

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.135-green?style=for-the-badge&logo=fastapi)
![Streamlit](https://img.shields.io/badge/Streamlit-1.56-red?style=for-the-badge&logo=streamlit)
![Groq](https://img.shields.io/badge/Groq-LLaMA_3.1-orange?style=for-the-badge)

**An intelligent career platform that analyzes your resume, finds relevant jobs, and prepares you for interviews — all powered by AI.**

</div>

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 📄 **Resume Analyzer** | Upload your PDF resume and get a detailed AI analysis — strengths, weaknesses, skill gaps, and suggestions |
| 🔍 **Resume-Based Job Search** | Finds and ranks jobs based on your actual resume skills with a smart match score |
| 🔎 **Custom Job Search** | Search by role, location, job type, and date with filters |
| 🎤 **AI Interview Prep** | Generates personalized interview questions (HR/Technical, Easy/Medium/Hard) and evaluates your answers |
| 💾 **Saved Jobs** | Save and revisit job listings you're interested in |

---

## 🛠️ Tech Stack

**Backend**
- [FastAPI](https://fastapi.tiangolo.com/) — REST API
- [Groq](https://groq.com/) — LLM inference (LLaMA 3.1 8B)
- [Sentence Transformers](https://www.sbert.net/) — Semantic similarity & job ranking
- [spaCy](https://spacy.io/) — NLP / skill extraction
- [FAISS](https://github.com/facebookresearch/faiss) — Vector search
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) — Job scraping
- [SerpAPI](https://serpapi.com/) — Google Jobs integration
- [PyMuPDF](https://pymupdf.readthedocs.io/) — PDF parsing

**Frontend**
- [Streamlit](https://streamlit.io/) — Interactive web UI

---

## 📁 Project Structure

```
JOB_SEARCH_ASSISTANT/
├── api.py                  # FastAPI backend — all endpoints
├── app.py                  # Streamlit frontend — UI
├── requirements.txt        # Python dependencies
├── render.yaml             # Render deployment config
├── saved_jobs.json         # Local saved jobs storage
└── utils/
    ├── resume_parser.py    # PDF text + skill extraction
    ├── resume_analyzer.py  # AI resume analysis (Groq)
    ├── job_search_agent.py # Job scraping + ranking logic
    ├── interview_agent.py  # Question generation + evaluation
    └── saved_jobs.py       # Save/retrieve jobs
```

---

## ⚙️ API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/parse-resume` | Upload PDF → extract text + skills |
| `POST` | `/analyze-resume` | AI analysis of resume for a target role |
| `GET`  | `/jobs` | Custom job search with filters |
| `POST` | `/top-jobs` | Resume-based ranked job search |
| `POST` | `/save-job` | Save a job listing |
| `GET`  | `/saved-jobs` | Get all saved jobs |
| `POST` | `/generate-questions` | Generate interview questions |
| `POST` | `/evaluate` | Evaluate interview answers |

Interactive API docs: `http://localhost:8000/docs`

---

## 🚀 Run Locally

### Prerequisites
- Python 3.10+
- Groq API key → [console.groq.com](https://console.groq.com)
- SerpAPI key (optional) → [serpapi.com](https://serpapi.com)

### Setup

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/ai-job-search-assistant.git
cd ai-job-search-assistant

# 2. Create virtual environment
python3 -m venv .venv
source .venv/bin/activate        # macOS/Linux
# .venv\Scripts\activate         # Windows

# 3. Install dependencies
pip install -r requirements.txt
python -m spacy download en_core_web_sm

# 4. Create .env file
echo "GROQ_API_KEY=your_groq_key_here" > .env
echo "SERP_API_KEY=your_serp_key_here" >> .env

# 5. Start backend (Terminal 1)
uvicorn api:app --reload --port 8000

# 6. Start frontend (Terminal 2)
streamlit run app.py --server.fileWatcherType none
```

Open **http://localhost:8501** in your browser.

---

## 🌐 Deployment (Render)

### Architecture
- **FastAPI backend** → Render Web Service (Starter plan)
- **Streamlit frontend** → Render Web Service (Free plan)

### Environment Variables

**Backend service:**
```
GROQ_API_KEY=your_groq_key
SERP_API_KEY=your_serp_key
PYTHONUNBUFFERED=1
TRANSFORMERS_CACHE=/tmp/hf_cache
HF_HOME=/tmp/hf_home
```

**Frontend service:**
```
BACKEND_URL=https://your-backend-name.onrender.com
PYTHONUNBUFFERED=1
```

See the full deployment guide in `deployment_guide.md`.

---

## 📸 Screenshots

> Resume Analyzer · Job Search · Interview Prep

*(Add screenshots here after deployment)*

---

## 🔑 API Keys

| Service | Free Tier | Get Key |
|---------|-----------|---------|
| Groq (LLM) | Very generous free limits | [console.groq.com](https://console.groq.com) |
| SerpAPI (Google Jobs) | 100 searches/month | [serpapi.com](https://serpapi.com) |

> **Note:** The app works without a SerpAPI key — LinkedIn, Indeed, Naukri, Remotive, and Google scraping still work as fallback sources.

---

## ⚠️ Known Limitations

- **Saved jobs** are stored in a local JSON file. On Render free tier, they reset on redeploy. For persistent storage, a database integration is recommended.
- **Web scraping** results depend on site availability. Some job sources may return fewer results depending on rate limits.
- **SerpAPI** free tier allows 100 Google Jobs searches per month.

---

## 📄 License

MIT License — feel free to use, modify, and distribute.

---

<div align="center">
Built with ❤️ using FastAPI · Streamlit · Groq · SentenceTransformers
</div>
