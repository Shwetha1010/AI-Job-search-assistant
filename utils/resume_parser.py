#resume_parser.py
import fitz  # PyMuPDF
import re
import spacy
from sentence_transformers import SentenceTransformer, util

# Load models
nlp = spacy.load("en_core_web_sm")
model = SentenceTransformer('all-MiniLM-L6-v2')

# -----------------------------
# IT SKILLS DATABASE
# -----------------------------
IT_SKILLS = [
    # Programming
    "python", "java", "c++", "javascript", "rust",

    # Data Science
    "pandas", "numpy", "scikit-learn", "matplotlib", "seaborn",

    # ML / AI
    "machine learning", "deep learning", "nlp", "computer vision",
    "tensorflow", "pytorch",

    # Web Dev
    "html", "css", "react", "node.js", "flask", "django",

    # Databases
    "mysql", "postgresql", "mongodb", "sqlite",

    # Cloud / DevOps
    "aws", "docker", "kubernetes", "ci/cd",

        # Tools
    "git", "linux", "api", "streamlit",

    # AI / LLM
    "langchain",
    "rag",
    "hugging face",
    "transformers",
    "prompt engineering",
    "llm",

    # Deployment
    "fastapi",

    # Data
    "sql",
    "power bi",

    # Computer Vision
    "opencv",
    "yolo",

    # Deep Learning
    "keras"
]

# Precompute embeddings
skill_embeddings = model.encode(IT_SKILLS, convert_to_tensor=True)

# -----------------------------
# TEXT EXTRACTION
# -----------------------------
def extract_text_from_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text.lower()

# -----------------------------
# CLEAN TEXT
# -----------------------------
def clean_text(text):
    text = re.sub(r'\n', ' ', text)
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    return text

# -----------------------------
# KEYWORD MATCHING
# -----------------------------
def keyword_skill_extraction(text):
    found_skills = []
    for skill in IT_SKILLS:
        if skill in text:
            found_skills.append(skill)
    return list(set(found_skills))

# -----------------------------
# SEMANTIC MATCHING
# -----------------------------
def semantic_skill_extraction(text):
    sentences = [sent.text for sent in nlp(text).sents]

    detected_skills = set()

    for sentence in sentences:
        sent_embedding = model.encode(sentence, convert_to_tensor=True)
        similarities = util.cos_sim(sent_embedding, skill_embeddings)

        for idx, score in enumerate(similarities[0]):
            if score > 0.75:  # threshold
                detected_skills.add(IT_SKILLS[idx])

    return list(detected_skills)

# -----------------------------
# MAIN FUNCTION
# -----------------------------
def parse_resume(file):
    text = extract_text_from_pdf(file)
    text = clean_text(text)

    keyword_skills = keyword_skill_extraction(text)
    semantic_skills = semantic_skill_extraction(text)

    all_skills = list(set(keyword_skills + semantic_skills))

    return {
        "text": text,
        "skills": all_skills
    }