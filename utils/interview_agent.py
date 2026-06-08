# interview_agent.py
from groq import Groq
import os
import re
import json
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# ==============================
# QUESTION GENERATION
# ==============================
def generate_questions(skills, job_role, interview_type, difficulty, jd_text=""):

    skills_str = ", ".join(skills) if skills else "general skills"
    role_str = job_role if job_role else "the applied role"

    # -------------------------------------------------------
    # HR INTERVIEW PROMPTS  (difficulty-aware)
    # -------------------------------------------------------
    if interview_type == "HR":

        if difficulty == "Easy":
            focus = (
                "Focus on introductory behavioral questions suitable for freshers or entry-level candidates:\n"
                "- Self-introduction and background\n"
                "- Basic teamwork and communication experiences\n"
                "- Simple situational questions ('What would you do if...')\n"
                "- Career goals and motivation\n"
                "- Learning from small challenges"
            )
            tone = "Keep questions simple, friendly, and non-intimidating."

        elif difficulty == "Medium":
            focus = (
                "Focus on mid-level behavioral and situational questions using the STAR method:\n"
                "- Conflict resolution with teammates or stakeholders\n"
                "- Handling competing priorities and tight deadlines\n"
                "- Leading a small initiative or cross-functional project\n"
                "- Handling negative feedback or failure\n"
                "- Communicating complex issues to non-technical stakeholders\n"
                "- Adapting to sudden changes in project requirements"
            )
            tone = "Questions should feel like they come from a mid-level HR screening round."

        else:  # Hard
            focus = (
                "Focus on senior-level behavioral and leadership questions:\n"
                "- Leading large teams or high-stakes projects under pressure\n"
                "- Strategic decisions with incomplete information\n"
                "- Managing disagreements with senior leadership\n"
                "- Influencing org-wide change or process improvements\n"
                "- Ethical dilemmas and professional integrity\n"
                "- Long-term career vision and impact"
            )
            tone = "Questions should feel like they come from a senior leadership or final HR round."

        prompt = f"""You are an experienced HR interviewer conducting a {difficulty}-level behavioral interview.

Candidate Profile:
- Target Role: {role_str}
- Skills & Background: {skills_str}

{focus}

{tone}

STRICT RULES:
- Generate exactly 10 questions.
- ONLY behavioral / situational questions — NO technical definitions.
- Tailor every question to the candidate's role ({role_str}) and background ({skills_str}).
- Use natural, conversational interview language.
- Each question MUST end with a '?'.
- DO NOT include numbering (1., 2., etc.), bullet points, or any explanation.
- Return ONLY the questions, one per line.

Generate the 10 questions now:"""

    # -------------------------------------------------------
    # TECHNICAL INTERVIEW PROMPTS  (difficulty-aware)
    # -------------------------------------------------------
    else:

        if difficulty == "Easy":
            focus = (
                "Focus on fundamentals and beginner-level technical questions:\n"
                "- Core concepts and definitions of key skills\n"
                "- Basic syntax and usage of mentioned technologies\n"
                "- Simple project questions ('What did you build? What was your role?')\n"
                "- Basic data structures and algorithms\n"
                "- Introductory tool/library usage"
            )
            tone = "Questions should feel like a screening or entry-level technical round."

        elif difficulty == "Medium":
            focus = (
                "Focus on practical implementation and real-world problem-solving:\n"
                "- Design decisions made in past projects\n"
                "- Trade-offs between different approaches or libraries\n"
                "- Debugging and performance tuning scenarios\n"
                "- API design, data pipelines, or system integration\n"
                "- Real-world usage of the candidate's listed skills\n"
                "- Code reviews or best-practice questions"
            )
            tone = "Questions should feel like a practical technical interview for a mid-level position."

        else:  # Hard
            focus = (
                "Focus on advanced system design, optimization, and deep reasoning:\n"
                "- Large-scale system design questions relevant to the role\n"
                "- Performance bottlenecks, scalability, and fault tolerance\n"
                "- Edge cases, failure modes, and recovery strategies\n"
                "- Trade-offs between consistency, availability, and partition tolerance\n"
                "- Advanced algorithm design and complexity analysis\n"
                "- Architecture decisions and technical leadership"
            )
            tone = "Questions should feel like a senior/staff-level technical interview."

        prompt = f"""You are a senior technical interviewer conducting a {difficulty}-level interview.

Candidate Profile:
- Target Role: {role_str}
- Skills & Technologies: {skills_str}
{f'- Job Description Context: {jd_text[:500]}' if jd_text else ''}

{focus}

{tone}

STRICT RULES:
- Generate exactly 10 questions.
- ONLY technical questions — NO behavioral questions.
- Every question must be directly related to the candidate's skills ({skills_str}) or role ({role_str}).
- Mix concept questions, scenario questions, and project-based questions.
- Each question MUST end with a '?'.
- DO NOT include numbering, bullet points, or any explanation.
- Return ONLY the questions, one per line.

Generate the 10 questions now:"""

    # -------------------------------------------------------
    # LLM CALL
    # -------------------------------------------------------
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8
        )
        text = response.choices[0].message.content.strip()
    except Exception as e:
        print("Groq error in generate_questions:", e)
        text = ""

    # -------------------------------------------------------
    # ROBUST EXTRACTION — keep only lines ending with '?'
    # -------------------------------------------------------
    questions = re.findall(r'[^\n?]*\?', text)
    questions = [q.strip().lstrip("•-0123456789. ") for q in questions if len(q.strip()) > 15]

    # -------------------------------------------------------
    # FALLBACK QUESTIONS (difficulty + type aware)
    # -------------------------------------------------------
    if len(questions) < 5:
        primary_skill = skills[0] if skills else "your primary skill"

        if interview_type == "HR":
            if difficulty == "Easy":
                questions = [
                    f"Can you introduce yourself and tell us why you're interested in the {role_str} role?",
                    "Describe a time you worked as part of a team on a project?",
                    f"What motivated you to learn {primary_skill}?",
                    "How do you manage your time when working on multiple tasks?",
                    "Describe a challenge you faced in a project and how you overcame it?",
                    "How do you handle feedback from a senior or mentor?",
                    "Tell me about a goal you set and how you achieved it?",
                    f"Why do you think you are a good fit for the {role_str} position?",
                    "How do you stay updated with new developments in your field?",
                    "Where do you see yourself professionally in the next two years?"
                ]
            elif difficulty == "Medium":
                questions = [
                    f"Tell me about a time you had to meet a tight deadline on a {role_str} related project?",
                    "Describe a conflict with a teammate and how you resolved it?",
                    f"Give an example where you used {primary_skill} to solve a real business problem?",
                    "Tell me about a time your project requirements changed unexpectedly?",
                    "Describe a situation where you had to present technical work to a non-technical audience?",
                    "Tell me about a time you failed and what you learned from it?",
                    "How do you prioritize tasks when everything seems equally urgent?",
                    "Describe a time you influenced a team decision without formal authority?",
                    "Tell me about a project you are most proud of and why?",
                    "How do you handle situations where you disagree with your manager's decision?"
                ]
            else:  # Hard
                questions = [
                    f"Tell me about a time you led a high-stakes {role_str} project under significant pressure?",
                    "Describe a situation where you had to make a major strategic decision with incomplete data?",
                    "Tell me about a time you had to manage a serious disagreement with senior leadership?",
                    "How have you driven an org-wide process change or cultural shift?",
                    "Describe the most complex stakeholder management challenge you have faced?",
                    "Tell me about a time your ethical judgment was tested in a professional setting?",
                    "How do you coach or mentor someone who is underperforming?",
                    "Describe a time you had to deliver very difficult news to your team or client?",
                    "What is the most impactful contribution you have made in your career so far?",
                    "Where do you want to take your career in the long term and how does this role fit?"
                ]
        else:  # Technical
            if difficulty == "Easy":
                questions = [
                    f"Can you explain what {primary_skill} is and how you have used it?",
                    f"What is your experience with the {role_str} role?",
                    "What are the most common data structures you have worked with?",
                    f"Walk me through a simple project you built using {primary_skill}?",
                    "What is the difference between supervised and unsupervised learning?",
                    "How do you approach debugging an error in your code?",
                    "What tools or IDEs do you use for development and why?",
                    "Can you explain what an API is and how you have used one?",
                    "What is version control and how do you use Git?",
                    f"What resources do you use to learn more about {primary_skill}?"
                ]
            elif difficulty == "Medium":
                questions = [
                    f"How would you design a data pipeline using {primary_skill} for a production system?",
                    "What trade-offs did you consider when choosing a library or framework in a past project?",
                    f"Describe a real-world problem you solved using {primary_skill} and your approach?",
                    "How do you handle missing data in a machine learning pipeline?",
                    "What is overfitting and what techniques have you used to prevent it?",
                    "How would you evaluate and compare two different models?",
                    f"Can you walk me through the architecture of a project you built involving {primary_skill}?",
                    "How do you optimize a slow SQL query or database operation?",
                    "What is cross-validation and when would you use k-fold vs stratified k-fold?",
                    "How do you approach feature engineering for a new dataset?"
                ]
            else:  # Hard
                questions = [
                    f"How would you design a scalable, fault-tolerant system for a {role_str} use case handling millions of requests?",
                    f"What are the key architectural trade-offs when deploying {primary_skill} models at scale?",
                    "How would you handle data drift in a production machine learning system?",
                    "Design a real-time recommendation system — what components would you include?",
                    "How do you ensure reproducibility and versioning of ML experiments in production?",
                    "What strategies would you use to reduce inference latency for a deep learning model?",
                    "How would you architect a system that must balance consistency vs availability?",
                    f"Describe the most complex technical problem you have solved involving {primary_skill} and your solution approach?",
                    "How would you design an A/B testing framework for a machine learning product?",
                    "What are the security and privacy considerations when building AI systems on user data?"
                ]

    return questions[:10]


# ==============================
# ANSWER EVALUATION
# ==============================
def evaluate_answers(questions, answers):

    qa_text = "\n\n".join([
        f"Q{i+1}: {q}\nA{i+1}: {a if a.strip() else '[No answer provided]'}"
        for i, (q, a) in enumerate(zip(questions, answers))
    ])

    prompt = f"""You are an expert interview coach evaluating a candidate's interview performance.

Interview Q&A:
{qa_text}

Evaluate the candidate's performance and return a JSON object with EXACTLY this structure:

{{
  "overall_score": <number from 0 to 10, one decimal place>,
  "individual_scores": [
    {{
      "question": "<question text>",
      "score": <number from 0 to 10>,
      "feedback": "<1-2 sentence specific feedback on this answer>"
    }}
  ],
  "strengths": [
    "<specific strength observed across answers>",
    "<another strength>"
  ],
  "weaknesses": [
    "<specific weakness observed>",
    "<another weakness if any>"
  ],
  "suggestions": [
    "<actionable suggestion to improve>",
    "<another suggestion>"
  ],
  "areas_to_improve": [
    "<topic or skill area the candidate should study or practice>",
    "<another area>"
  ]
}}

STRICT RULES:
- Return ONLY valid JSON. No markdown, no explanation, no preamble.
- overall_score must reflect the average quality across all answers.
- Be honest but constructive — evaluate like a real senior interviewer.
- If an answer is blank or says 'No answer provided', give a score of 0 for that question.
- strengths, weaknesses, suggestions, and areas_to_improve must each have at least 2 items."""

    raw = ""  # initialise so it's always bound
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        raw = response.choices[0].message.content.strip()

        # Strip markdown code fences if present
        raw = re.sub(r"^```(?:json)?\s*", "", raw)
        raw = re.sub(r"\s*```$", "", raw)

        result = json.loads(raw)
        return result

    except json.JSONDecodeError:
        return {
            "overall_score": 0.0,
            "individual_scores": [],
            "strengths": ["Could not parse structured evaluation."],
            "weaknesses": ["Response from AI was not valid JSON."],
            "suggestions": ["Please try again."],
            "areas_to_improve": ["N/A"],
            "raw_response": raw          # always defined now
        }
    except Exception as e:
        print("Groq error in evaluate_answers:", e)
        return {
            "overall_score": 0.0,
            "individual_scores": [],
            "strengths": [],
            "weaknesses": [],
            "suggestions": ["Backend error during evaluation. Please retry."],
            "areas_to_improve": [],
        }