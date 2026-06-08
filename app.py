# app.py
import os
import requests
import streamlit as st

BASE_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000").strip()

# ─────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────
st.set_page_config(
    page_title="AI Job Search Assistant",
    page_icon="🤖",
    layout="wide"
)

# ─────────────────────────────────────
# GLOBAL CSS
# ─────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* ── Base ── */
html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }

.stApp {
    background: linear-gradient(135deg, #0d0f1a 0%, #111827 60%, #0d1321 100%);
    color: #e2e8f0;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #111827 0%, #1a2035 100%) !important;
    border-right: 1px solid rgba(99,102,241,0.2);
}
section[data-testid="stSidebar"] .stSelectbox label,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] h1 {
    color: #a5b4fc !important;
    font-weight: 600;
}

/* ── Headings ── */
h1 { color: #c7d2fe !important; font-weight: 800 !important; letter-spacing: -0.5px; }
h2 { color: #a5b4fc !important; font-weight: 700 !important; }
h3 { color: #818cf8 !important; font-weight: 600 !important; }

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.5rem 1.5rem !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 15px rgba(99,102,241,0.3) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(99,102,241,0.5) !important;
}

/* ── Inputs ── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: #1e2535 !important;
    border: 1px solid rgba(99,102,241,0.3) !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
    padding: 0.6rem 1rem !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 2px rgba(99,102,241,0.2) !important;
}

/* ── Selectbox ── */
.stSelectbox > div > div {
    background: #1e2535 !important;
    border: 1px solid rgba(99,102,241,0.3) !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
}

/* ── File uploader ── */
[data-testid="stFileUploader"] {
    background: #1a2035 !important;
    border: 2px dashed rgba(99,102,241,0.4) !important;
    border-radius: 12px !important;
    padding: 1rem !important;
}

/* ── Expander ── */
.streamlit-expanderHeader {
    background: #1e2535 !important;
    border-radius: 10px !important;
    color: #a5b4fc !important;
    font-weight: 500 !important;
}
.streamlit-expanderContent {
    background: #161c2d !important;
    border-radius: 0 0 10px 10px !important;
    border: 1px solid rgba(99,102,241,0.15) !important;
}

/* ── Metric ── */
[data-testid="metric-container"] {
    background: linear-gradient(135deg, #1e2535 0%, #252d40 100%);
    border: 1px solid rgba(99,102,241,0.3);
    border-radius: 12px;
    padding: 1rem;
}
[data-testid="metric-container"] label { color: #a5b4fc !important; }
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #c7d2fe !important;
    font-size: 2rem !important;
    font-weight: 700 !important;
}

/* ── Alerts ── */
.stSuccess { background: rgba(16,185,129,0.15) !important; border-left: 4px solid #10b981 !important; border-radius: 8px !important; }
.stWarning { background: rgba(245,158,11,0.15) !important; border-left: 4px solid #f59e0b !important; border-radius: 8px !important; }
.stError   { background: rgba(239,68,68,0.15)  !important; border-left: 4px solid #ef4444 !important; border-radius: 8px !important; }
.stInfo    { background: rgba(99,102,241,0.15)  !important; border-left: 4px solid #6366f1 !important; border-radius: 8px !important; }

/* ── Divider ── */
hr { border-color: rgba(99,102,241,0.2) !important; }

/* ── Custom card classes ── */
.job-card {
    background: linear-gradient(135deg, #1a2035 0%, #1e2844 100%);
    border: 1px solid rgba(99,102,241,0.2);
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    transition: all 0.2s ease;
    box-shadow: 0 4px 20px rgba(0,0,0,0.3);
}
.job-card:hover { border-color: rgba(99,102,241,0.5); transform: translateY(-2px); box-shadow: 0 8px 30px rgba(99,102,241,0.15); }

.job-title {
    font-size: 1.15rem;
    font-weight: 700;
    color: #c7d2fe;
    margin-bottom: 0.4rem;
}
.job-meta {
    font-size: 0.85rem;
    color: #94a3b8;
    margin-bottom: 0.6rem;
    display: flex;
    flex-wrap: wrap;
    gap: 0.8rem;
}
.score-badge {
    display: inline-block;
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    color: white;
    font-size: 0.8rem;
    font-weight: 700;
    padding: 0.25rem 0.75rem;
    border-radius: 20px;
    margin-bottom: 0.6rem;
}
.tag {
    display: inline-block;
    background: rgba(99,102,241,0.15);
    color: #a5b4fc;
    font-size: 0.75rem;
    font-weight: 500;
    padding: 0.2rem 0.6rem;
    border-radius: 6px;
    border: 1px solid rgba(99,102,241,0.25);
    margin: 0.2rem;
}
.apply-btn {
    display: inline-block;
    background: linear-gradient(135deg, #10b981, #059669);
    color: white !important;
    text-decoration: none !important;
    padding: 0.45rem 1.2rem;
    border-radius: 8px;
    font-weight: 600;
    font-size: 0.85rem;
    transition: all 0.2s;
    box-shadow: 0 4px 12px rgba(16,185,129,0.3);
}
.apply-btn:hover { box-shadow: 0 6px 20px rgba(16,185,129,0.5); transform: translateY(-1px); }

.feature-card {
    background: linear-gradient(135deg, #1a2035 0%, #1e2844 100%);
    border: 1px solid rgba(99,102,241,0.2);
    border-radius: 16px;
    padding: 1.8rem 1.5rem;
    text-align: center;
    transition: all 0.2s ease;
    box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    height: 100%;
}
.feature-card:hover { border-color: #6366f1; transform: translateY(-4px); box-shadow: 0 12px 40px rgba(99,102,241,0.2); }
.feature-icon { font-size: 2.5rem; margin-bottom: 0.8rem; }
.feature-title { font-size: 1.05rem; font-weight: 700; color: #c7d2fe; margin-bottom: 0.5rem; }
.feature-desc { font-size: 0.85rem; color: #94a3b8; line-height: 1.5; }

.section-header {
    background: linear-gradient(135deg, #1a2035, #252d40);
    border-left: 4px solid #6366f1;
    padding: 0.8rem 1.2rem;
    border-radius: 0 10px 10px 0;
    margin-bottom: 1rem;
    font-size: 1.05rem;
    font-weight: 700;
    color: #c7d2fe;
}
.skill-pill {
    display: inline-block;
    background: rgba(99,102,241,0.15);
    color: #a5b4fc;
    border: 1px solid rgba(99,102,241,0.3);
    padding: 0.3rem 0.8rem;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 500;
    margin: 0.2rem;
}
.question-card {
    background: linear-gradient(135deg, #1a2035, #1e2844);
    border: 1px solid rgba(99,102,241,0.2);
    border-radius: 12px;
    padding: 1.2rem;
    margin-bottom: 0.8rem;
}
.q-number {
    display: inline-block;
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    color: white;
    font-weight: 700;
    font-size: 0.8rem;
    padding: 0.2rem 0.6rem;
    border-radius: 6px;
    margin-bottom: 0.5rem;
}
.q-text { font-size: 0.95rem; font-weight: 600; color: #c7d2fe; }

.eval-card {
    border-radius: 12px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.6rem;
    font-size: 0.9rem;
    font-weight: 500;
}
.eval-strength { background: rgba(16,185,129,0.12); border: 1px solid rgba(16,185,129,0.3); color: #6ee7b7; }
.eval-weakness { background: rgba(245,158,11,0.12); border: 1px solid rgba(245,158,11,0.3); color: #fcd34d; }
.eval-suggestion{ background: rgba(99,102,241,0.12); border: 1px solid rgba(99,102,241,0.3); color: #a5b4fc; }
.eval-area { background: rgba(148,163,184,0.08); border: 1px solid rgba(148,163,184,0.2); color: #94a3b8; }

.hero-title {
    font-size: 3rem;
    font-weight: 800;
    background: linear-gradient(135deg, #818cf8, #c084fc, #38bdf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.2;
    margin-bottom: 1rem;
}
.hero-subtitle { font-size: 1.1rem; color: #94a3b8; max-width: 600px; margin-bottom: 2rem; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────
with st.sidebar:
    st.markdown("## 🚀 Navigation")
    page = st.selectbox(
        "Go to",
        ["🏠 Home", "📄 Resume Analyzer", "🔍 Job Search", "🎤 Interview Prep", "💾 Saved Jobs"]
    )

# ─────────────────────────────────────
# HOME PAGE
# ─────────────────────────────────────
if page == "🏠 Home":

    st.markdown('<div class="hero-title">AI Job Search Assistant</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="hero-subtitle">Your intelligent career partner — powered by AI to help you land your dream job faster.</div>',
        unsafe_allow_html=True
    )

    c1, c2, c3, c4 = st.columns(4)
    cards = [
        ("📄", "Resume Analyzer",  "Upload your resume and get an in-depth AI analysis with skill gaps and suggestions."),
        ("🔍", "Smart Job Search", "Find relevant jobs matched to your resume or search by role, location, and type."),
        ("🎤", "Interview Prep",   "Practice with AI-generated questions at your chosen difficulty and get scored feedback."),
        ("💾", "Saved Jobs",       "Track and revisit jobs you've saved, all in one organised place."),
    ]
    for col, (icon, title, desc) in zip([c1, c2, c3, c4], cards):
        with col:
            st.markdown(
                f'<div class="feature-card">'
                f'<div class="feature-icon">{icon}</div>'
                f'<div class="feature-title">{title}</div>'
                f'<div class="feature-desc">{desc}</div>'
                f'</div>',
                unsafe_allow_html=True
            )

    st.markdown("<br>", unsafe_allow_html=True)
    st.info("👈 Use the sidebar to navigate between features.")

# ─────────────────────────────────────
# RESUME ANALYZER PAGE
# ─────────────────────────────────────
elif page == "📄 Resume Analyzer":

    st.markdown("# 📄 Resume Analyzer")
    st.markdown('<div style="color:#94a3b8;margin-bottom:1.5rem">Get a detailed, personalized AI analysis of your resume for any target role.</div>', unsafe_allow_html=True)

    col_left, col_right = st.columns([1, 1], gap="large")

    with col_left:
        uploaded_file = st.file_uploader("📎 Upload your resume (PDF)", type=["pdf"])
        job_role      = st.text_input("🎯 Target job role", placeholder="e.g. Data Scientist, Software Engineer")

        analyze_btn = st.button("🔍 Analyze Resume", use_container_width=True)

    with col_right:
        st.markdown(
            '<div class="feature-card" style="text-align:left">'
            '<div class="feature-icon">💡</div>'
            '<div class="feature-title">What you\'ll get</div>'
            '<div class="feature-desc">'
            '✅ Overall resume strength summary<br>'
            '✅ Evidence-based strengths<br>'
            '✅ Clear weakness identification<br>'
            '✅ Missing skill gaps for the role<br>'
            '✅ Actionable improvement suggestions'
            '</div></div>',
            unsafe_allow_html=True
        )

    if analyze_btn:
        if uploaded_file and job_role:
            with st.spinner("🧠 Analyzing your resume…"):
                try:
                    res    = requests.post(f"{BASE_URL}/parse-resume", files={"file": uploaded_file})
                    parsed = res.json()
                    res2   = requests.post(
                        f"{BASE_URL}/analyze-resume",
                        json={"text": parsed["text"], "skills": parsed["skills"], "role": job_role}
                    )
                    analysis = res2.json()
                except Exception as e:
                    st.error(f"❌ Backend error: {e}\n\nBackend URL being used: {BASE_URL}")
                    st.stop()

            st.success("✅ Analysis Complete!")

            # Skills display
            st.markdown('<div class="section-header">📌 Detected Skills</div>', unsafe_allow_html=True)
            skills = parsed.get("skills", [])
            if skills:
                pills = "".join(f'<span class="skill-pill">{s}</span>' for s in skills)
                st.markdown(f'<div style="margin-bottom:1rem">{pills}</div>', unsafe_allow_html=True)
            else:
                st.caption("No skills extracted.")

            # Analysis result
            st.markdown('<div class="section-header">🧠 AI Analysis</div>', unsafe_allow_html=True)
            st.markdown(
                f'<div class="job-card" style="font-size:0.92rem;line-height:1.8;color:#cbd5e1">{analysis}</div>',
                unsafe_allow_html=True
            )
        else:
            st.warning("⚠️ Please upload a resume and enter a job role.")

# ─────────────────────────────────────
# JOB SEARCH PAGE
# ─────────────────────────────────────
elif page == "🔍 Job Search":

    st.markdown("# 🔍 Job Search")
    st.markdown('<div style="color:#94a3b8;margin-bottom:1.5rem">Find jobs matched to your resume or search with custom filters.</div>', unsafe_allow_html=True)

    mode = st.radio("Search Mode", ["🎯 Resume Based", "🔎 Custom Search"], horizontal=True, label_visibility="collapsed")

    st.markdown("---")

    # ── helper to render a job card ──────────────────────────────────
    def render_job_card(job, i, mode_prefix):
        score = job.get("score", 0) or 0
        link  = job.get("link", "").strip()

        score_color = "#10b981" if score >= 70 else "#f59e0b" if score >= 40 else "#ef4444"
        score_html  = (
            f'<span class="score-badge" style="background:linear-gradient(135deg,{score_color},{score_color}cc)">'
            f'🎯 {score}% Match</span>'
        ) if score else ""

        tag_type = f'<span class="tag">💼 {job.get("type","N/A")}</span>' if job.get("type") else ""
        tag_src  = f'<span class="tag">🔗 {job.get("source","")}</span>' if job.get("source") else ""
        tag_date = f'<span class="tag">📅 {job.get("posted_at","Unknown")}</span>'

        apply_html = (
            f'<a class="apply-btn" href="{link}" target="_blank" rel="noopener noreferrer">🔗 Apply Here</a>'
            if link and link.startswith("http")
            else '<span style="color:#64748b;font-size:0.8rem">No direct link available</span>'
        )

        st.markdown(
            f'<div class="job-card">'
            f'<div class="job-title">{job.get("title","N/A")}</div>'
            f'<div class="job-meta">'
            f'🏢 <b>{job.get("company","N/A")}</b> &nbsp;|&nbsp; '
            f'📍 {job.get("location","N/A")}'
            f'</div>'
            f'{score_html}&nbsp;{tag_type}{tag_src}{tag_date}'
            f'</div>',
            unsafe_allow_html=True
        )

        exp_col, btn_col, link_col = st.columns([3, 1, 1])
        with exp_col:
            with st.expander("📄 View Description"):
                st.write(job.get("description", "No description available"))
        with btn_col:
            if st.button("💾 Save", key=f"save_{mode_prefix}_{i}"):
                try:
                    resp   = requests.post(f"{BASE_URL}/save-job", json=job, timeout=5)
                    result = resp.json()
                    if result.get("message") == "duplicate":
                        st.info("Already saved!")
                    elif resp.status_code == 200:
                        st.success("✅ Saved!")
                    else:
                        st.error("❌ Failed")
                except Exception as e:
                    st.error(f"Error: {e}")
        with link_col:
            st.markdown(apply_html, unsafe_allow_html=True)

        st.markdown("<div style='margin-bottom:0.5rem'></div>", unsafe_allow_html=True)

    # ── RESUME BASED ─────────────────────────────────────────────────
    if mode == "🎯 Resume Based":

        uploaded_file = st.file_uploader("📎 Upload Resume", type=["pdf"])
        job_role      = st.text_input("🎯 Enter Job Role (optional)", placeholder="e.g. Machine Learning Engineer")

        if st.button("🔍 Find Matching Jobs", use_container_width=True):
            if not uploaded_file:
                st.warning("Please upload a resume")
                st.stop()

            with st.spinner("🧠 Parsing resume and finding personalized jobs…"):
                try:
                    res         = requests.post(f"{BASE_URL}/parse-resume", files={"file": uploaded_file})
                    parsed      = res.json()
                    user_skills = parsed.get("skills", [])
                    search_role = job_role.strip() if job_role.strip() else "data scientist"

                    res2 = requests.post(
                        f"{BASE_URL}/top-jobs",
                        json={"skills": user_skills, "role": search_role, "location": "India"}
                    )
                    jobs = res2.json()

                    if isinstance(jobs, dict):
                        st.error(f"API Error: {jobs}")
                        st.stop()

                except Exception as e:
                    st.error(f"Backend not running or error occurred: {e}")
                    st.stop()

            st.session_state.resume_jobs        = jobs
            st.session_state.resume_user_skills = user_skills

        if "resume_jobs" in st.session_state:
            jobs        = st.session_state.resume_jobs
            user_skills = st.session_state.get("resume_user_skills", [])

            if not jobs:
                st.warning("No matching jobs found.")
            else:
                st.success(f"✅ Found {len(jobs)} personalized job matches!")
                if user_skills:
                    pills = "".join(f'<span class="skill-pill">{s}</span>' for s in user_skills[:12])
                    st.markdown(f'<div style="margin-bottom:1rem">Your skills: {pills}</div>', unsafe_allow_html=True)

                for i, job in enumerate(jobs):
                    if isinstance(job, dict):
                        render_job_card(job, i, "resume")

    # ── CUSTOM SEARCH ─────────────────────────────────────────────────
    elif mode == "🔎 Custom Search":

        if "custom_role"     not in st.session_state: st.session_state.custom_role     = ""
        if "custom_location" not in st.session_state: st.session_state.custom_location = "All India"
        if "custom_type"     not in st.session_state: st.session_state.custom_type     = "Any"
        if "custom_days"     not in st.session_state: st.session_state.custom_days     = "Any"

        c1, c2 = st.columns(2)
        with c1:
            role = st.text_input("💼 Job Role", value=st.session_state.custom_role, placeholder="e.g. Data Analyst")
            job_type = st.selectbox("🏠 Job Type", ["Any", "Remote", "Hybrid", "Onsite"])
        with c2:
            state = st.selectbox("📍 Location", [
                "All India", "Andhra Pradesh", "Telangana", "Karnataka", "Tamil Nadu",
                "Maharashtra", "Delhi", "Uttar Pradesh", "Gujarat", "Rajasthan",
                "West Bengal", "Kerala", "Punjab", "Haryana", "Odisha", "Bihar",
                "Madhya Pradesh", "Jharkhand", "Chhattisgarh", "Assam"
            ])
            days = st.selectbox("📅 Posted Within", ["Any", "1 day", "7 days", "30 days"])

        if st.button("🔎 Search Jobs", use_container_width=True):
            if not role.strip():
                st.warning("Please enter a job role")
                st.stop()

            st.session_state.custom_role     = role
            st.session_state.custom_location = state
            st.session_state.custom_type     = job_type
            st.session_state.custom_days     = days

            with st.spinner("🔍 Searching jobs…"):
                try:
                    res = requests.get(
                        f"{BASE_URL}/jobs",
                        params={"role": role, "location": state, "days": days, "job_type": job_type}
                    )
                    if res.status_code != 200:
                        st.error(f"API Error: {res.status_code}")
                        st.stop()

                    jobs = res.json()
                    if not isinstance(jobs, list):
                        st.error("Invalid response from API")
                        st.stop()

                    st.session_state.custom_jobs = jobs
                except Exception as e:
                    st.error(f"Backend not running: {e}")
                    st.stop()

        if "custom_jobs" in st.session_state:
            jobs = st.session_state.custom_jobs

            if not jobs:
                st.warning("No jobs found for the selected filters.")
            else:
                st.success(f"✅ Found {len(jobs)} jobs")
                for i, job in enumerate(jobs):
                    if isinstance(job, dict):
                        render_job_card(job, i, "custom")

# ─────────────────────────────────────
# INTERVIEW PREP PAGE
# ─────────────────────────────────────
elif page == "🎤 Interview Prep":

    st.markdown("# 🎤 AI Interview Agent")
    st.markdown('<div style="color:#94a3b8;margin-bottom:1.5rem">Practice with AI-generated questions and get detailed performance feedback.</div>', unsafe_allow_html=True)

    col_form, col_tip = st.columns([2, 1], gap="large")

    with col_form:
        uploaded_file  = st.file_uploader("📎 Upload Resume", type=["pdf"])
        job_role       = st.text_input("🎯 Job Role", placeholder="e.g. Backend Developer")
        c1, c2 = st.columns(2)
        with c1:
            interview_type = st.selectbox("🗂 Interview Type", ["HR", "Technical"])
        with c2:
            difficulty = st.selectbox("📊 Difficulty", ["Easy", "Medium", "Hard"])

    with col_tip:
        diff_colors = {"Easy": "#10b981", "Medium": "#f59e0b", "Hard": "#ef4444"}
        d_color     = diff_colors.get(difficulty if 'difficulty' in dir() else "Easy", "#6366f1")
        st.markdown(
            f'<div class="feature-card" style="text-align:left">'
            f'<div class="feature-icon">🎯</div>'
            f'<div class="feature-title">Interview Tips</div>'
            f'<div class="feature-desc">'
            f'• Be specific and use examples<br>'
            f'• Show problem-solving process<br>'
            f'• Relate answers to the job role<br>'
            f'• For HR: focus on soft skills<br>'
            f'• For Tech: explain your reasoning'
            f'</div></div>',
            unsafe_allow_html=True
        )

    if st.button("🎤 Start Interview", use_container_width=True):

        if not uploaded_file:
            st.warning("Please upload your resume.")
            st.stop()
        if not job_role.strip():
            st.warning("Please enter a job role.")
            st.stop()

        with st.spinner("🧠 Generating interview questions…"):
            try:
                res    = requests.post(f"{BASE_URL}/parse-resume", files={"file": uploaded_file})
                parsed = res.json()

                res2 = requests.post(
                    f"{BASE_URL}/generate-questions",
                    json={
                        "skills":     parsed.get("skills", []),
                        "role":       job_role,
                        "type":       interview_type,
                        "difficulty": difficulty
                    }
                )
                questions = res2.json()

                if not isinstance(questions, list) or not questions:
                    st.error("Could not generate questions. Please try again.")
                    st.stop()

            except Exception as e:
                st.error(f"Backend error: {e}")
                st.stop()

        # ── TASK 1 FIX: clear old text-area widget states before new session ──
        # st.text_area widgets store values under st.session_state["ans_0"] etc.
        # Resetting answers=[] alone doesn't clear widget state — must delete keys.
        if "questions" in st.session_state:
            for idx in range(len(st.session_state.questions)):
                st.session_state.pop(f"ans_{idx}", None)

        st.session_state.questions     = questions
        st.session_state.answers       = [""] * len(questions)
        st.session_state.result        = None
        st.session_state.parsed_skills = parsed.get("skills", [])

    # ── SHOW QUESTIONS ────────────────────────────────────────────────
    if "questions" in st.session_state and st.session_state.questions:

        st.markdown("---")
        st.markdown('<div class="section-header">📝 Answer the following questions</div>', unsafe_allow_html=True)

        for i, q in enumerate(st.session_state.questions):
            st.markdown(
                f'<div class="question-card">'
                f'<span class="q-number">Q{i+1}</span>'
                f'<div class="q-text">{q}</div>'
                f'</div>',
                unsafe_allow_html=True
            )
            st.session_state.answers[i] = st.text_area(
                "Your Answer",
                value=st.session_state.answers[i],
                key=f"ans_{i}",
                height=100,
                label_visibility="collapsed",
                placeholder="Type your answer here…"
            )

        if st.button("📊 Evaluate My Answers", use_container_width=True):
            with st.spinner("📊 Evaluating your responses…"):
                try:
                    res = requests.post(
                        f"{BASE_URL}/evaluate",
                        json={"questions": st.session_state.questions, "answers": st.session_state.answers}
                    )
                    st.session_state.result = res.json()
                except Exception as e:
                    st.error(f"Evaluation failed: {e}")

    # ── SHOW EVALUATION RESULTS ────────────────────────────────────────
    if "result" in st.session_state and st.session_state.result:
        result = st.session_state.result

        st.markdown("---")
        st.markdown('<div class="section-header">📊 Interview Evaluation Report</div>', unsafe_allow_html=True)

        overall = result.get("overall_score", "N/A")
        score_v = float(overall) if isinstance(overall, (int, float)) else 0
        score_color = "#10b981" if score_v >= 7 else "#f59e0b" if score_v >= 5 else "#ef4444"

        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric("🏆 Overall Score", f"{overall} / 10")
        with m2:
            individual = result.get("individual_scores", [])
            st.metric("📋 Questions Answered", len(individual))
        with m3:
            avg_q = round(sum(x.get("score", 0) for x in individual) / len(individual), 1) if individual else 0
            st.metric("📈 Avg. Question Score", f"{avg_q} / 10")

        # Per-question breakdown
        if individual:
            st.markdown('<div class="section-header">📋 Question-by-Question Breakdown</div>', unsafe_allow_html=True)
            for idx, item in enumerate(individual):
                q_score = item.get("score", "N/A")
                q_color = "#10b981" if (isinstance(q_score, (int,float)) and q_score>=7) else "#f59e0b" if (isinstance(q_score,(int,float)) and q_score>=5) else "#ef4444"
                with st.expander(f"Q{idx+1}: {item.get('question','')[:80]}…  |  Score: {q_score}/10"):
                    st.write(item.get("feedback", ""))

        c1, c2 = st.columns(2)
        with c1:
            strengths = result.get("strengths", [])
            if strengths:
                st.markdown('<div class="section-header">✅ Strengths</div>', unsafe_allow_html=True)
                for s in strengths:
                    st.markdown(f'<div class="eval-card eval-strength">✅ {s}</div>', unsafe_allow_html=True)

            suggestions = result.get("suggestions", [])
            if suggestions:
                st.markdown('<div class="section-header">💡 Suggestions</div>', unsafe_allow_html=True)
                for s in suggestions:
                    st.markdown(f'<div class="eval-card eval-suggestion">💡 {s}</div>', unsafe_allow_html=True)

        with c2:
            weaknesses = result.get("weaknesses", [])
            if weaknesses:
                st.markdown('<div class="section-header">⚠️ Weaknesses</div>', unsafe_allow_html=True)
                for w in weaknesses:
                    st.markdown(f'<div class="eval-card eval-weakness">⚠️ {w}</div>', unsafe_allow_html=True)

            areas = result.get("areas_to_improve", [])
            if areas:
                st.markdown('<div class="section-header">📚 Areas to Improve</div>', unsafe_allow_html=True)
                for a in areas:
                    st.markdown(f'<div class="eval-card eval-area">📚 {a}</div>', unsafe_allow_html=True)

        if "raw_response" in result:
            with st.expander("Raw AI Response"):
                st.text(result["raw_response"])

# ─────────────────────────────────────
# SAVED JOBS PAGE
# ─────────────────────────────────────
elif page == "💾 Saved Jobs":

    st.markdown("# 💾 Saved Jobs")
    st.markdown('<div style="color:#94a3b8;margin-bottom:1.5rem">Your bookmarked opportunities, all in one place.</div>', unsafe_allow_html=True)

    try:
        res  = requests.get(f"{BASE_URL}/saved-jobs")
        jobs = res.json()
        if isinstance(jobs, dict):
            st.error(f"API Error: {jobs}")
            st.stop()
    except Exception:
        st.error("Backend not running")
        st.stop()

    if jobs:
        st.success(f"📌 {len(jobs)} saved job(s)")
        for job in jobs:
            if not isinstance(job, dict):
                continue

            link = job.get("link", "").strip()
            apply_html = (
                f'<a class="apply-btn" href="{link}" target="_blank" rel="noopener noreferrer">🔗 Apply Here</a>'
                if link and link.startswith("http")
                else '<span style="color:#64748b;font-size:0.8rem">No direct link</span>'
            )

            st.markdown(
                f'<div class="job-card">'
                f'<div class="job-title">{job.get("title","N/A")}</div>'
                f'<div class="job-meta">'
                f'🏢 <b>{job.get("company","N/A")}</b> &nbsp;|&nbsp; '
                f'📍 {job.get("location","N/A")} &nbsp;|&nbsp; '
                f'💼 {job.get("type","N/A")} &nbsp;|&nbsp; '
                f'📅 {job.get("posted_at","Unknown")}'
                f'</div>'
                f'{apply_html}'
                f'</div>',
                unsafe_allow_html=True
            )
            with st.expander("📄 View Description"):
                st.write(job.get("description", "No description available"))
            st.markdown("<div style='margin-bottom:0.5rem'></div>", unsafe_allow_html=True)
    else:
        st.markdown(
            '<div class="feature-card" style="max-width:400px;margin:2rem auto;text-align:center">'
            '<div class="feature-icon">🔖</div>'
            '<div class="feature-title">No saved jobs yet</div>'
            '<div class="feature-desc">Find jobs in Job Search and click Save to bookmark them here.</div>'
            '</div>',
            unsafe_allow_html=True
        )