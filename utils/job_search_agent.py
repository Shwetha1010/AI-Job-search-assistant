# job_search_agent.py
# ==============================
# IMPORTS
# ==============================
import os
import requests
import numpy as np
import random
import re
from dotenv import load_dotenv

load_dotenv()

from bs4 import BeautifulSoup
from serpapi.google_search import GoogleSearch
from sentence_transformers import SentenceTransformer, util

# ==============================
# MODEL
# ==============================
model = SentenceTransformer('all-MiniLM-L6-v2')

SERP_API_KEY = os.getenv("SERP_API_KEY", "")  # Add SERP_API_KEY to your .env file

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

# ==============================
# STATE → CITY ALIAS MAP
# (Bug 2 fix: location filtering)
# ==============================
STATE_CITY_MAP = {
    "karnataka":        ["bengaluru", "bangalore", "mysore", "mysuru", "hubli", "dharwad", "mangalore", "karnataka"],
    "maharashtra":      ["mumbai", "pune", "nagpur", "thane", "nashik", "aurangabad", "solapur", "maharashtra"],
    "telangana":        ["hyderabad", "secunderabad", "warangal", "karimnagar", "nizamabad", "telangana"],
    "andhra pradesh":   ["visakhapatnam", "vijayawada", "guntur", "nellore", "tirupati", "kurnool", "andhra pradesh"],
    "tamil nadu":       ["chennai", "coimbatore", "madurai", "salem", "trichy", "tiruchirappalli", "tamil nadu"],
    "delhi":            ["new delhi", "delhi", "noida", "gurugram", "gurgaon", "faridabad"],
    "uttar pradesh":    ["lucknow", "kanpur", "agra", "varanasi", "allahabad", "meerut", "uttar pradesh"],
    "gujarat":          ["ahmedabad", "surat", "vadodara", "rajkot", "gandhinagar", "gujarat"],
    "rajasthan":        ["jaipur", "jodhpur", "udaipur", "kota", "ajmer", "rajasthan"],
    "west bengal":      ["kolkata", "calcutta", "howrah", "durgapur", "asansol", "west bengal"],
    "kerala":           ["thiruvananthapuram", "trivandrum", "kochi", "cochin", "kozhikode", "calicut", "kerala"],
    "punjab":           ["chandigarh", "ludhiana", "amritsar", "jalandhar", "patiala", "punjab"],
    "haryana":          ["gurugram", "gurgaon", "faridabad", "ambala", "rohtak", "haryana"],
    "odisha":           ["bhubaneswar", "cuttack", "rourkela", "puri", "odisha"],
    "bihar":            ["patna", "gaya", "bhagalpur", "muzaffarpur", "bihar"],
    "madhya pradesh":   ["bhopal", "indore", "jabalpur", "gwalior", "madhya pradesh"],
    "jharkhand":        ["ranchi", "jamshedpur", "dhanbad", "bokaro", "jharkhand"],
    "chhattisgarh":     ["raipur", "bhilai", "bilaspur", "durg", "chhattisgarh"],
    "assam":            ["guwahati", "silchar", "dibrugarh", "assam"],
}

def location_matches(job_location: str, selected_state: str) -> bool:
    """Return True if job_location is within selected_state (using alias map)."""
    if selected_state.lower() == "all india":
        return True
    job_loc_lower = job_location.lower()
    state_key = selected_state.lower()
    aliases = STATE_CITY_MAP.get(state_key, [state_key])
    return any(alias in job_loc_lower for alias in aliases)


# ==============================
# JOB TYPE DETECTION
# ==============================
def detect_job_type(title, description):
    text = f"{title} {description}".lower()
    if any(x in text for x in ["remote", "work from home", "wfh", "fully remote"]):
        return "Remote"
    if any(x in text for x in ["hybrid", "flexible location"]):
        return "Hybrid"
    if any(x in text for x in ["onsite", "on-site", "in office", "in-office", "office only"]):
        return "Onsite"
    return "N/A"


# ==============================
# SCRAPE REAL JOB DESCRIPTION
# ==============================
def scrape_job_description(url):
    try:
        if not url or "http" not in url:
            return ""
        res = requests.get(url, headers=HEADERS, timeout=5)
        soup = BeautifulSoup(res.text, "lxml")

        selectors = [
            ".job-description",
            ".description",
            ".jobDescriptionText",
            ".show-more-less-html__markup",
            ".dang-inner-html",
            "[data-testid='job-description']",
            "#job-description",
        ]
        for sel in selectors:
            tag = soup.select_one(sel)
            if tag:
                text = tag.get_text(" ", strip=True)
                if len(text) > 200:
                    return text[:2000]
        return ""
    except:
        return ""


# ==============================
# FALLBACK DESCRIPTION GENERATOR
# (role-aware so descriptions don't all look the same)
# ==============================
def generate_description(role, title=""):
    role_skill_map = {
        "data analyst":        ["SQL", "Excel", "Power BI", "Tableau", "Python", "Statistics", "Data Visualization"],
        "data scientist":      ["Python", "Machine Learning", "TensorFlow", "Scikit-learn", "Statistics", "NLP", "Deep Learning"],
        "machine learning":    ["Python", "PyTorch", "TensorFlow", "MLOps", "Scikit-learn", "Feature Engineering"],
        "software engineer":   ["Java", "Python", "System Design", "REST APIs", "Microservices", "Docker"],
        "frontend":            ["React", "JavaScript", "TypeScript", "CSS", "HTML", "UI/UX"],
        "backend":             ["Node.js", "Java", "Python", "Databases", "REST APIs", "Caching"],
        "devops":              ["Docker", "Kubernetes", "CI/CD", "AWS", "Terraform", "Linux"],
        "nlp":                 ["Python", "Transformers", "spaCy", "NLTK", "BERT", "LLMs"],
    }
    # pick the best matching skill set
    chosen_skills = ["Python", "SQL", "APIs", "Git", "Agile", "Communication"]
    for key, skills in role_skill_map.items():
        if key in (role + " " + title).lower():
            chosen_skills = skills
            break

    random.shuffle(chosen_skills)
    responsibilities = [
        f"Design and implement {title or role} solutions for real-world problems",
        "Collaborate with cross-functional teams to deliver high-quality outputs",
        "Analyze requirements and translate them into technical implementations",
        "Maintain and optimize existing systems for performance and reliability",
        "Document work and participate in code/design reviews",
    ]
    random.shuffle(responsibilities)

    return (
        f"Role: {title or role}\n\n"
        f"Responsibilities:\n"
        + "\n".join(f"- {r}" for r in responsibilities[:3])
        + f"\n\nSkills Required: {', '.join(chosen_skills[:5])}\n"
        f"Nice to Have: {', '.join(chosen_skills[5:])}"
    )


# ==============================
# 1. SERP API (Google Jobs)
# ==============================
def get_jobs_serp(role, location="India"):
    try:
        params = {
            "engine": "google_jobs",
            "q": role,
            "location": location,
            "api_key": SERP_API_KEY
        }
        search = GoogleSearch(params)
        results = search.get_dict()

        jobs = []
        for job in results.get("jobs_results", []):
            title = job.get("title", "N/A")
            link = job.get("related_links", [{}])[0].get("link", "")
            desc = job.get("description") or scrape_job_description(link)
            if not desc:
                desc = generate_description(role, title)

            job_type = detect_job_type(title, desc)
            posted = job.get("detected_extensions", {}).get("posted_at", "Unknown")

            jobs.append({
                "title": title,
                "company": job.get("company_name", "N/A"),
                "location": job.get("location", location),
                "link": link,
                "type": job_type,
                "posted_at": posted or "Unknown",
                "description": desc,
                "source": "Google Jobs"
            })
        return jobs
    except Exception as e:
        print("SERP API ERROR:", e)
        return []


# ==============================
# 2. INDEED SCRAPER
# ==============================
def scrape_indeed_jobs(role, location="India"):
    try:
        url = f"https://in.indeed.com/jobs?q={role}&l={location}"
        res = requests.get(url, headers=HEADERS, timeout=6)
        soup = BeautifulSoup(res.text, "lxml")

        jobs = []
        for card in soup.select(".job_seen_beacon")[:15]:
            title_tag = card.select_one("h2 span[title]") or card.select_one("h2 span")
            company_tag = card.select_one("[data-testid='company-name']") or card.select_one(".companyName")
            location_tag = card.select_one("[data-testid='text-location']") or card.select_one(".companyLocation")
            summary_tag = card.select_one(".job-snippet") or card.select_one(".underShelfFooter")

            title = title_tag.get("title") or title_tag.text.strip() if title_tag else "N/A"
            desc = summary_tag.text.strip() if summary_tag else generate_description(role, title)
            if len(desc) < 100:
                desc = generate_description(role, title)

            job_type = detect_job_type(title, desc)
            jobs.append({
                "title": title,
                "company": company_tag.text.strip() if company_tag else "N/A",
                "location": location_tag.text.strip() if location_tag else location,
                "link": "https://in.indeed.com",
                "type": job_type,
                "posted_at": "Unknown",
                "description": desc,
                "source": "Indeed"
            })
        return jobs
    except Exception as e:
        print("Indeed ERROR:", e)
        return []


# ==============================
# 3. LINKEDIN SCRAPER
# ==============================
def scrape_linkedin_jobs(role, location="India"):
    try:
        url = f"https://www.linkedin.com/jobs/search/?keywords={role}&location={location}"
        res = requests.get(url, headers=HEADERS, timeout=6)
        soup = BeautifulSoup(res.text, "lxml")

        jobs = []
        for job in soup.select(".base-card")[:15]:
            title_el  = job.select_one("h3.base-search-card__title")
            company_el = job.select_one("h4.base-search-card__subtitle")
            location_el = job.select_one(".job-search-card__location")
            link_el = job.select_one("a.base-card__full-link")

            title_text = title_el.text.strip() if title_el else "N/A"
            link_url   = link_el["href"] if link_el else ""
            loc_text   = location_el.text.strip() if location_el else location

            desc = scrape_job_description(link_url) or generate_description(role, title_text)
            job_type = detect_job_type(title_text, desc)

            jobs.append({
                "title": title_text,
                "company": company_el.text.strip() if company_el else "N/A",
                "location": loc_text,
                "link": link_url,
                "type": job_type,
                "posted_at": "Unknown",
                "description": desc,
                "source": "LinkedIn"
            })
        return jobs
    except Exception as e:
        print("LinkedIn ERROR:", e)
        return []


# ==============================
# 4. NAUKRI SCRAPER
# ==============================
def scrape_naukri_jobs(role, location="India"):
    try:
        role_clean = role.lower().replace(" ", "-")
        loc_clean  = location.lower().replace(" ", "-")
        url = f"https://www.naukri.com/{role_clean}-jobs-in-{loc_clean}"

        res = requests.get(url, headers=HEADERS, timeout=6)
        soup = BeautifulSoup(res.text, "lxml")

        jobs = []
        # Naukri uses multiple selectors across versions
        cards = soup.select(".jobTuple") or soup.select("article.jobTupleHeader") or []
        for job in cards[:15]:
            title_el   = job.select_one("a.title") or job.select_one(".title")
            company_el = job.select_one(".comp-name") or job.select_one(".companyInfo span")
            location_el = job.select_one(".locWdth") or job.select_one(".location span")

            title_text = title_el.text.strip() if title_el else "N/A"
            link_url   = title_el["href"] if title_el and title_el.has_attr("href") else ""

            desc = scrape_job_description(link_url) or generate_description(role, title_text)
            job_type = detect_job_type(title_text, desc)

            jobs.append({
                "title": title_text,
                "company": company_el.text.strip() if company_el else "N/A",
                "location": location_el.text.strip() if location_el else location,
                "link": link_url,
                "type": job_type,
                "posted_at": "Unknown",
                "description": desc,
                "source": "Naukri"
            })
        return jobs
    except Exception as e:
        print("Naukri ERROR:", e)
        return []


# ==============================
# 5. GOOGLE WEB SCRAPER
# ==============================
def scrape_google_jobs(role):
    try:
        query = f"site:linkedin.com/jobs OR site:naukri.com {role} jobs India"
        url = f"https://www.google.com/search?q={query}"
        res = requests.get(url, headers=HEADERS, timeout=6)
        soup = BeautifulSoup(res.text, "lxml")

        jobs = []
        for g in soup.select(".tF2Cxc")[:10]:
            title_el = g.select_one("h3")
            link_el  = g.select_one("a")
            if title_el and link_el:
                title_text = title_el.text.strip()
                link_url   = link_el["href"]
                desc = scrape_job_description(link_url) or generate_description(role, title_text)
                job_type = detect_job_type(title_text, desc)
                jobs.append({
                    "title": title_text,
                    "company": "From Web",
                    "location": "India",
                    "link": link_url,
                    "type": job_type,
                    "posted_at": "Unknown",
                    "description": desc,
                    "source": "Google"
                })
        return jobs
    except Exception as e:
        print("Google scrape error:", e)
        return []


# ==============================
# 6. REMOTIVE API
# (Bug 5 fix: token-based partial match)
# ==============================
def get_remotive_jobs(role):
    try:
        url = "https://remotive.com/api/remote-jobs"
        response = requests.get(url, timeout=10)
        data = response.json()

        role_tokens = set(role.lower().split())
        jobs = []

        for job in data.get("jobs", []):
            title = job.get("title", "")
            title_tokens = set(title.lower().split())

            # At least one meaningful token must match
            if not role_tokens.intersection(title_tokens):
                continue

            # Strip HTML from description
            raw_desc = job.get("description", "")
            if raw_desc:
                soup = BeautifulSoup(raw_desc, "lxml")
                desc = soup.get_text(" ", strip=True)[:2000]
            else:
                desc = generate_description(role, title)

            pub_date = str(job.get("publication_date", "Unknown"))

            jobs.append({
                "title": title,
                "company": job.get("company_name", "N/A"),
                "location": "Remote",
                "link": job.get("url", ""),
                "type": "Remote",
                "posted_at": pub_date,
                "description": desc,
                "source": "Remotive"
            })
        return jobs
    except Exception as e:
        print("Remotive Error:", e)
        return []


# ==============================
# FILTER BY POSTED DAYS
# (Bug fix: keep jobs with unknown dates, mark them clearly)
# ==============================
def filter_by_days(jobs, days):
    if not days or days == "Any":
        return jobs

    try:
        limit = int(days.split()[0])
    except (ValueError, IndexError):
        return jobs

    filtered = []
    for job in jobs:
        posted = str(job.get("posted_at", "")).lower().strip()

        # Unknown date → keep it but mark clearly
        if not posted or posted in ("unknown", "n/a", ""):
            job = dict(job)
            job["posted_at"] = "Unknown"
            filtered.append(job)
            continue

        # "X days ago" or "X day ago"
        if "day" in posted:
            match = re.search(r"(\d+)", posted)
            if match and int(match.group(1)) <= limit:
                filtered.append(job)
            continue

        # ISO date string like "2024-06-01T…"
        if re.match(r"\d{4}-\d{2}-\d{2}", posted):
            from datetime import datetime, timezone
            try:
                pub = datetime.fromisoformat(posted[:10])
                delta = (datetime.now() - pub).days
                if delta <= limit:
                    filtered.append(job)
            except:
                job = dict(job)
                job["posted_at"] = "Unknown"
                filtered.append(job)
            continue

        # If we can't parse, keep but mark unknown
        job = dict(job)
        job["posted_at"] = "Unknown"
        filtered.append(job)

    return filtered


# ==============================
# REMOVE DUPLICATES
# (Bug fix: normalize key before comparison)
# ==============================
def remove_duplicates(jobs):
    seen = set()
    unique = []
    for job in jobs:
        # Normalize: lowercase, strip spaces
        title_norm   = re.sub(r"\s+", " ", str(job.get("title", "")).lower().strip())
        company_norm = re.sub(r"\s+", " ", str(job.get("company", "")).lower().strip())
        key = (title_norm, company_norm)
        if key not in seen:
            seen.add(key)
            unique.append(job)
    return unique


# ==============================
# FILTER BY JOB TYPE (backend)
# (Bug 3 fix: job_type filtering moved to backend)
# ==============================
def filter_by_job_type(jobs, job_type):
    if not job_type or job_type == "Any":
        return jobs
    filtered = []
    for job in jobs:
        jt = str(job.get("type", "")).lower()
        # Allow "N/A" (type unknown) to pass through so we don't hide real jobs
        if jt in ("n/a", "", "unknown") or job_type.lower() in jt:
            filtered.append(job)
    return filtered


# ==============================
# ROLE RELEVANCE FILTER
# (New: for custom search ranking — Bug 4 partial fix)
# ==============================
def filter_by_role_relevance(jobs, role, threshold=0.25):
    """Rank jobs by title ↔ role similarity. Jobs below threshold are sorted last."""
    if not role or not jobs:
        return jobs

    role_emb  = model.encode(role, convert_to_tensor=True)
    titles    = [job.get("title", "") for job in jobs]
    title_embs = model.encode(titles, convert_to_tensor=True)

    sims = util.cos_sim(role_emb, title_embs)[0].cpu().numpy()

    # Attach relevance score
    scored = []
    for i, job in enumerate(jobs):
        scored.append((sims[i], job))

    # Sort: relevant first, irrelevant last
    scored.sort(key=lambda x: x[0], reverse=True)

    return [j for _, j in scored]


# ==============================
# FALLBACK JOBS
# ==============================
def get_dummy_jobs(role):
    jobs = []
    companies = ["Infosys", "TCS", "Wipro", "HCL", "Cognizant", "Accenture"]
    for i in range(8):
        title = role.title()
        desc  = generate_description(role, title)
        jobs.append({
            "title": title,
            "company": random.choice(companies),
            "location": "India",
            "link": "https://www.naukri.com/",
            "type": detect_job_type(title, desc),
            "posted_at": "Unknown",
            "description": desc,
            "source": "Fallback"
        })
    return jobs


# ==============================
# MAIN PIPELINE
# (Bug 1+2+3 fix: accepts job_type; uses alias-based location; backend filtering)
# ==============================
def get_all_jobs(role, location="India", days="Any", job_type="Any"):
    if not role or role.strip() == "":
        role = "software engineer"

    jobs = []
    try:
        jobs += get_jobs_serp(role, location)
        jobs += scrape_linkedin_jobs(role, location)
        jobs += scrape_naukri_jobs(role, location)
        jobs += scrape_indeed_jobs(role, location)
        jobs += scrape_google_jobs(role)
        jobs += get_remotive_jobs(role)
    except Exception as e:
        print("Scraping ERROR:", e)

    # Deduplicate
    jobs = remove_duplicates(jobs)

    # Location filter — alias-based
    if location and location.lower() not in ("all india", "india", ""):
        jobs = [j for j in jobs if location_matches(str(j.get("location", "")), location)]

    # Job type filter — backend
    jobs = filter_by_job_type(jobs, job_type)

    # Date filter
    jobs = filter_by_days(jobs, days)

    # Fallback if too few results
    if len(jobs) < 5:
        print("⚠️ Using fallback jobs")
        jobs += get_dummy_jobs(role)
        jobs = remove_duplicates(jobs)

    return jobs


# ==============================
# MATCH SCORE — hybrid 70% keyword + 30% semantic
# Fix: pure cosine-sim of short tokens vs long docs gives artificially low scores
# ==============================
def calculate_match(user_skills, job_text, job_title=""):
    """
    Returns a 0-100 score.
    70% — keyword overlap: how many user skills appear in job text / title
    30% — semantic similarity: embedding cosine sim as secondary signal
    """
    if not user_skills:
        return 0

    combined_text = f"{job_title} {job_text}".lower()

    # 70% — keyword overlap
    matched = sum(
        1 for skill in user_skills
        if skill.lower().strip() and skill.lower().strip() in combined_text
    )
    keyword_score = matched / len(user_skills) if user_skills else 0.0

    # 30% — semantic similarity
    semantic_score = 0.0
    if job_text and len(job_text.strip()) > 10:
        try:
            skills_emb    = model.encode(" ".join(user_skills), convert_to_tensor=True)
            job_emb       = model.encode(job_text[:1500], convert_to_tensor=True)
            semantic_score = float(util.cos_sim(skills_emb, job_emb))
            semantic_score = max(0.0, min(1.0, semantic_score))
        except Exception:
            semantic_score = 0.0

    final = 0.70 * keyword_score + 0.30 * semantic_score
    return round(final * 100, 1)


# ==============================
# WEIGHTED TOP JOBS (50/30/20)
# (Bug 4 fix: role-relevance dominates ranking)
# ==============================
def get_top_jobs(user_skills, jobs, model, role="", top_k=10):
    """
    Weighted ranking:
      50% — job title  ↔ target role similarity
      30% — job desc   ↔ resume skills similarity
      20% — job desc   ↔ full query (role + skills) similarity
    """
    if not jobs:
        return []

    # Filter to jobs that have a description
    valid_jobs = [j for j in jobs if j.get("description")]
    if not valid_jobs:
        return jobs[:top_k]

    descriptions = [j["description"] for j in valid_jobs]
    titles       = [j.get("title", "") for j in valid_jobs]

    # Encode role
    role_emb  = model.encode(role if role else " ".join(user_skills[:3]))

    # Encode full query (role + skills)
    full_query = f"{role} {' '.join(user_skills)}"
    query_emb  = model.encode(full_query)

    # Encode descriptions and titles in batch
    desc_embs  = model.encode(descriptions)
    title_embs = model.encode(titles)

    # Encode skills individually for skill-match score
    skill_embs = model.encode(user_skills) if user_skills else None

    final_scores = []
    for i in range(len(valid_jobs)):
        # 50% — role ↔ title
        title_sim = float(util.cos_sim(role_emb, title_embs[i]))

        # 30% — skills ↔ description
        if skill_embs is not None and len(skill_embs) > 0:
            skill_sims = [float(util.cos_sim(se, desc_embs[i])) for se in skill_embs]
            skill_sim  = float(np.mean(skill_sims))
        else:
            skill_sim = 0.0

        # 20% — full query ↔ description
        desc_sim = float(util.cos_sim(query_emb, desc_embs[i]))

        weighted = 0.5 * title_sim + 0.3 * skill_sim + 0.2 * desc_sim
        final_scores.append(weighted)

    ranked_indices = np.argsort(final_scores)[::-1]
    return [valid_jobs[i] for i in ranked_indices[:top_k]]