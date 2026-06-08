from fastapi import FastAPI, UploadFile, File
from typing import List
import uvicorn
import io

# Load sentence transformer model once at startup
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')

# Import modules
from utils.job_search_agent import get_all_jobs, get_top_jobs, calculate_match, filter_by_role_relevance
from utils.resume_parser import parse_resume
from utils.resume_analyzer import analyze_resume
from utils.interview_agent import generate_questions, evaluate_answers
from utils.saved_jobs import save_job, get_saved_jobs

app = FastAPI()


# -----------------------------
# JOB SEARCH
# -----------------------------
@app.get("/jobs")
def get_jobs(
    role: str,
    location: str = "India",
    days: str = "Any",          # Bug 1 fix: was missing → filters never reached backend
    job_type: str = "Any"       # Bug 3 fix: was missing → job type filter never reached backend
):
    jobs = get_all_jobs(role, location, days, job_type)

    # For custom search: re-rank by role relevance so the most relevant titles appear first
    if role:
        jobs = filter_by_role_relevance(jobs, role)

    return jobs


@app.post("/top-jobs")
def top_jobs(data: dict):
    skills   = data.get("skills", [])
    role     = data.get("role", "data scientist")
    location = data.get("location", "India")

    jobs     = get_all_jobs(role, location)
    ranked   = get_top_jobs(skills, jobs, model=model, role=role, top_k=10)

    # Attach match score to each job (pass title so keyword match includes it)
    for job in ranked:
        job["score"] = calculate_match(
            skills,
            job.get("description", ""),
            job_title=job.get("title", "")
        )

    return ranked


# -----------------------------
# SAVE JOBS
# -----------------------------
@app.post("/save-job")
def save(job: dict):
    print("🔥 API CALLED /save-job")
    result = save_job(job)
    return result          # now returns {"message": "saved"} or {"message": "duplicate"}


@app.get("/saved-jobs")
def saved_jobs_api():
    return get_saved_jobs()


# -----------------------------
# RESUME
# -----------------------------
@app.post("/parse-resume")
async def parse(file: UploadFile = File(...)):
    content = await file.read()
    result = parse_resume(io.BytesIO(content))
    return result


@app.post("/analyze-resume")
def analyze(data: dict):
    return analyze_resume(
        data["text"],
        data["skills"],
        data["role"]
    )


# -----------------------------
# INTERVIEW
# -----------------------------
@app.post("/generate-questions")
def questions(data: dict):
    return generate_questions(
        data["skills"],
        data["role"],
        data["type"],
        data["difficulty"]
    )


@app.post("/evaluate")
def evaluate(data: dict):
    return evaluate_answers(
        data["questions"],
        data["answers"]
    )


# -----------------------------
# RUN (DEV ONLY)
# -----------------------------
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)