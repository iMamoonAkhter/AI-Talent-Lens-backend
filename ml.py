import pdfplumber
import re

# -------------------------------
# 🔥 FIELD-WISE SKILLS DATASET
# -------------------------------

FIELDS = {
    "CS": [
        "python", "java", "c++", "c#", "javascript",
        "data structures", "algorithms", "oop",
        "dbms", "sql", "mysql", "mongodb",
        "operating systems", "computer networks",
        "software development", "problem solving",
        "debugging", "git", "github",
        "api development", "rest api",
        "multithreading", "system programming"
    ],

    "IT": [
        "networking", "tcp/ip", "dns", "dhcp",
        "cloud computing", "aws", "azure", "google cloud",
        "linux", "windows server", "system administration",
        "it support", "technical support",
        "troubleshooting", "hardware", "software installation",
        "network configuration", "firewalls", "vpn",
        "cyber infrastructure", "help desk"
    ],

    "AI": [
        "machine learning", "deep learning", "nlp",
        "computer vision", "neural networks",
        "tensorflow", "pytorch", "keras",
        "model training", "model evaluation",
        "feature engineering", "data preprocessing",
        "reinforcement learning", "ai models",
        "chatbot development", "image processing"
    ],

    "Data Science": [
        "python", "r", "pandas", "numpy",
        "data analysis", "data cleaning",
        "data visualization", "matplotlib", "seaborn",
        "statistics", "hypothesis testing",
        "machine learning", "regression", "classification",
        "power bi", "excel", "sql",
        "data storytelling", "dashboarding"
    ],

    "Cyber Security": [
        "ethical hacking", "penetration testing",
        "network security", "cyber security",
        "cryptography", "kali linux",
        "vulnerability assessment", "risk analysis",
        "firewalls", "intrusion detection",
        "malware analysis", "security auditing",
        "incident response", "digital forensics",
        "security policies", "siem tools"
    ],

    "SE": [
        "software engineering", "agile", "scrum",
        "software development lifecycle", "sdlc",
        "testing", "unit testing", "integration testing",
        "debugging", "system design",
        "design patterns", "version control",
        "git", "github",
        "requirements analysis", "uml diagrams",
        "software architecture", "code review"
    ],

    "Business Analytics": [
        "data analysis", "business intelligence",
        "excel", "advanced excel",
        "power bi", "tableau",
        "sql", "data visualization",
        "dashboarding", "reporting",
        "data storytelling", "kpi analysis",
        "forecasting", "trend analysis",
        "decision making", "business reporting"
    ],

    "BBA": [
        "management", "business management",
        "marketing", "digital marketing",
        "finance", "accounting",
        "human resource", "hr", "recruitment",
        "leadership", "communication",
        "sales", "negotiation",
        "business strategy", "project management",
        "customer relationship", "operations management"
    ],

    "BA": [
        "writing", "content writing",
        "research", "academic writing",
        "critical thinking", "analysis",
        "communication", "presentation skills",
        "editing", "proofreading",
        "report writing", "literature review",
        "social research", "qualitative analysis"
    ],

    "MBBS": [
        "anatomy", "physiology", "biochemistry", "pathology",
        "pharmacology", "clinical", "diagnosis", "surgery",
        "medicine", "patient care", "hospital", "doctor",
        "medical", "healthcare", "treatment",

        "patient examination", "clinical procedures", "iv cannulation",
        "injections", "bp monitoring", "emergency case handling",
        "medical report writing", "patient counseling",
        "ward rounds", "case documentation", "team collaboration",

        "basic life support", "bls", "first aid", "emergency response"
    ]
}

# -------------------------------
# 📄 PDF TEXT EXTRACTION
# -------------------------------
def extract_text(pdf_file):
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text.lower()

# -------------------------------
# 🧠 SKILL EXTRACTION (Regex)
# -------------------------------
def extract_skills(text):
    all_skills = []
    for field_skills in FIELDS.values():
        all_skills.extend(field_skills)

    found_skills = set()

    normalized_text = f" {text.lower()} "
    for skill in set(all_skills):
        skill_pattern = re.escape(skill.lower())
        # Match full tokens/phrases so partial words don't trigger false positives.
        if re.search(rf"(?<!\w){skill_pattern}(?!\w)", normalized_text):
            found_skills.add(skill)

    return list(found_skills)

# -------------------------------
# 🎓 EDUCATION EXTRACTION
# -------------------------------
def extract_education(text):
    edu_keywords = ["bs", "bachelor", "ms", "phd", "mbbs", "bba"]
    return [word for word in edu_keywords if word in text]

# -------------------------------
# 💼 EXPERIENCE EXTRACTION
# -------------------------------
def extract_experience(text):
    return re.findall(r'\d+\s+years?', text)

# -------------------------------
# 🎯 FIELD MATCHING
# -------------------------------
def match_field(user_skills):
    scores = {}

    for field, skills in FIELDS.items():
        match_count = len(set(user_skills) & set(skills))
        scores[field] = match_count

    best_field = max(scores, key=scores.get)
    return best_field, scores

# -------------------------------
# 📊 SKILL GAP ANALYSIS
# -------------------------------
def skill_gap(user_skills, field):
    required = set(FIELDS[field])
    return list(required - set(user_skills))

# -------------------------------
# 🎯 CV SCORE
# -------------------------------
def calculate_score(user_skills, field):
    required = set(FIELDS[field])
    if not required:
        return 0
    return round((len(set(user_skills) & required) / len(required)) * 100, 2)