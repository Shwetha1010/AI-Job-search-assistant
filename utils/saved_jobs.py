import json
import os
import re

# Bug 6 fix: use absolute path relative to THIS file so the JSON is always
# found regardless of which directory uvicorn is started from.
BASE_DIR  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILE_PATH = os.path.join(BASE_DIR, "saved_jobs.json")


def _normalize(text: str) -> str:
    """Lowercase + collapse whitespace for dedup comparison."""
    return re.sub(r"\s+", " ", str(text).lower().strip())


def save_job(job: dict) -> dict:
    print("🔥 SAVE FUNCTION TRIGGERED")
    print(f"   FILE_PATH = {FILE_PATH}")

    # Initialise file if missing
    if not os.path.exists(FILE_PATH):
        with open(FILE_PATH, "w") as f:
            json.dump([], f)

    with open(FILE_PATH, "r") as f:
        jobs = json.load(f)

    # Bug 6 fix: duplicate prevention
    new_title   = _normalize(job.get("title", ""))
    new_company = _normalize(job.get("company", ""))

    for existing in jobs:
        if (
            _normalize(existing.get("title", ""))   == new_title
            and _normalize(existing.get("company", "")) == new_company
        ):
            print("⚠️  Job already saved — skipping duplicate")
            return {"message": "duplicate", "detail": "Job already exists in saved list"}

    jobs.append(job)

    with open(FILE_PATH, "w") as f:
        json.dump(jobs, f, indent=2)

    print("✅ SAVED SUCCESSFULLY")
    return {"message": "saved"}


def get_saved_jobs() -> list:
    if not os.path.exists(FILE_PATH):
        return []
    with open(FILE_PATH, "r") as f:
        return json.load(f)