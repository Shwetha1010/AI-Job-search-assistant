<div align="center">

# 🤖 AI Job Search Assistant

### An end-to-end intelligent career platform powered by LLMs, semantic search, and real-time job scraping

[![Live Demo](https://img.shields.io/badge/🚀_Live_Demo-HuggingFace_Spaces-FFD21E?style=for-the-badge)](https://huggingface.co/spaces/sheethus/job-search-app)
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-FF4B4B?style=for-the-badge&logo=streamlit)](https://streamlit.io)
[![Groq](https://img.shields.io/badge/Groq-LLaMA_3.1-F54E00?style=for-the-badge)](https://groq.com)
[![HuggingFace](https://img.shields.io/badge/HuggingFace-Spaces-FFD21E?style=for-the-badge&logo=huggingface)](https://huggingface.co)

**[▶ Try the live app →](https://huggingface.co/spaces/sheethus/job-search-app)**

</div>

---

## What It Does

Upload your resume once. The system does the rest — analyzing your skills, finding matched jobs from across the web, and preparing you for interviews using AI.

| Module | What It Does |
|--------|-------------|
| **Resume Analyzer** | Parses your PDF, extracts skills with NLP, and generates a detailed AI analysis — strengths, gaps, and actionable suggestions |
| **Job Matcher** | Scrapes live jobs from LinkedIn, Indeed, Naukri & Google Jobs, then ranks them using a hybrid semantic + keyword scoring model |
| **Interview Coach** | Generates personalized interview questions (HR / Technical, Easy / Hard) based on your resume and target role, then evaluates your answers |
| **Saved Jobs** | Bookmark interesting roles and revisit them anytime |



---

## Tech Stack

**AI / ML**
- [Groq](https://groq.com) — Ultra-fast LLM inference with LLaMA 3.1 8B (resume analysis, interview Q&A)
- [Sentence Transformers](https://www.sbert.net) — `all-MiniLM-L6-v2` for semantic job-resume similarity
- [FAISS](https://github.com/facebookresearch/faiss) — Vector similarity search for skill matching
- [spaCy](https://spacy.io) — NLP pipeline for skill entity extraction
- Hybrid scoring: **70% keyword overlap + 30% semantic cosine similarity**

**Backend**
- [FastAPI](https://fastapi.tiangolo.com) — REST API with async support
- [PyMuPDF](https://pymupdf.readthedocs.io) — PDF parsing
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup) + [SerpAPI](https://serpapi.com) — Multi-source job scraping

**Frontend & Deployment**
- [Streamlit](https://streamlit.io) — Interactive UI
- [Docker](https://docker.com) — Containerised backend
- [HuggingFace Spaces](https://huggingface.co/spaces) — Free cloud hosting (16GB RAM)

---

## Run Locally

```bash
# Clone
git clone https://github.com/Shwetha1010/AI-Job-search-assistant.git
cd AI-Job-search-assistant

# Setup
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements-backend.txt
python -m spacy download en_core_web_sm

# Add API keys
echo "GROQ_API_KEY=your_key" > .env
echo "SERP_API_KEY=your_key" >> .env

# Start backend (Terminal 1)
uvicorn api:app --port 8000

# Start frontend (Terminal 2)
streamlit run app.py
```

Open `http://localhost:8501`

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/parse-resume` | Extract text and skills from PDF |
| `POST` | `/analyze-resume` | LLM-powered resume analysis |
| `POST` | `/top-jobs` | Semantically ranked job search |
| `GET`  | `/jobs` | Custom job search with filters |
| `POST` | `/generate-questions` | Personalized interview questions |
| `POST` | `/evaluate` | LLM evaluation of interview answers |
| `POST` | `/save-job` | Save a job listing |
| `GET`  | `/saved-jobs` | Retrieve saved jobs |

Interactive docs: `https://sheethus-job-search-api.hf.space/docs`

---

## Project Structure

```
├── api.py                    # FastAPI — all endpoints
├── app.py                    # Streamlit — UI
├── Dockerfile                # Backend container config
├── requirements.txt          # Frontend dependencies
├── requirements-backend.txt  # Backend + ML dependencies
└── utils/
    ├── resume_parser.py      # PDF parsing + NLP skill extraction
    ├── resume_analyzer.py    # Groq LLM analysis prompt
    ├── job_search_agent.py   # Scraping + hybrid ranking logic
    ├── interview_agent.py    # Question generation + evaluation
    └── saved_jobs.py         # Job persistence
```

---

<div align="center">

Built with Python · FastAPI · Streamlit · Groq · HuggingFace

**[▶ Try it live](https://huggingface.co/spaces/sheethus/job-search-app)**

</div>
