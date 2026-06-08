#resume_analyzer.py
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def analyze_resume(text, skills, job_role):

    skills_str = ", ".join(skills) if skills else "None detected"

    prompt = f"""You are a professional career coach and resume expert.

Analyze the resume below for the target role: {job_role}

Extracted Skills from resume: {skills_str}

Resume Text:
{text[:4000]}

---

STRICT RULES:
- Write ONLY based on what is present in the resume text and extracted skills above.
- Do NOT invent skills, certifications, projects, or experience that are not mentioned.
- Do NOT mention the candidate's name.
- Be specific — reference actual skills, projects, and experiences from the resume.
- Every strength and weakness must cite evidence from the resume.
- Be concise and direct — job seekers need actionable advice, not generic filler.
- If information is missing or unclear, say so honestly.

---

Produce a structured analysis with EXACTLY these 5 sections:

1. SUMMARY
Write 3-4 sentences: How strong is this resume for {job_role}? What is the overall profile — entry-level, mid-level, or experienced? What is the most impressive aspect?

2. STRENGTHS
List 3-5 specific strengths. For each:
- Name it clearly (e.g., "Strong Python background")
- Cite evidence from the resume (e.g., "Demonstrated through X project using Y")
- Explain why this matters for {job_role}

3. WEAKNESSES
List 2-4 specific weaknesses. For each:
- Name it (e.g., "No cloud deployment experience")
- Explain why it is a gap for {job_role}
- ONLY mention weaknesses clearly absent from the resume
- If no critical weaknesses, state: "No critical weaknesses identified for this role."

4. SKILL GAPS
List skills commonly required for {job_role} but NOT present in this resume.
Format: "Missing: [Skill] — Why it matters: [reason]"

5. SUGGESTIONS FOR IMPROVEMENT
Give 4-6 specific, actionable suggestions ranked by impact. Each must answer:
- What exactly should the candidate do?
- Which project, certification, or course would help most?
- How will this increase their chances for {job_role}?

Example: "Build a project using [specific tool] to demonstrate [skill]. Consider the Google Data Analytics Certificate on Coursera to fill the SQL and BI gap."

Write the full analysis now:"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4
    )

    return response.choices[0].message.content