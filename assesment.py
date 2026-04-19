from functools import lru_cache
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.preprocessing import MultiLabelBinarizer

# --- MASTER DATA & LOGIC CONFIG ---
MASTER_TECH_LIST = {
    "CS": ["python", "java", "c++", "dsa", "docker", "react", "system design", "javascript"],
    "AI": ["python", "math", "statistics", "ml", "machine learning", "deep learning", "dl", "nlp", "llms", "llm"],
    "Data Science": ["python", "sql", "pandas", "tableau", "big data", "deployment", "data visualization"],
    "Cyber Security": ["networking", "linux", "ethical hacking", "cryptography", "cyber security", "pentesting"],
    "SE": ["oop", "dsa", "testing", "agile", "devops", "ci/cd", "software engineering"],
    "Business Analytics": ["excel", "sql", "power bi", "predictive modeling", "business intelligence"],
    "IT": ["networking", "hardware", "operating systems", "cloud computing", "system administration", "security"]
}

ALL_FIELDS_DATA = {
    **MASTER_TECH_LIST,
    "MBBS": ["anatomy", "physiology", "biochemistry", "clinical practice", "surgery", "diagnosis", "medicine"],
    "BBA": ["management", "marketing", "business communication", "strategic management", "finance", "entrepreneurship"],
    "BA": ["communication", "writing", "critical thinking", "research", "analysis", "public speaking"]
}

ALL_WORTHY_SKILLS = set([skill for sublist in MASTER_TECH_LIST.values() for skill in sublist])

@lru_cache(maxsize=1)
def train_ml_engine(csv_path='skilldata.csv'):
    try:
        df = pd.read_csv(csv_path)
        df['Skill_List'] = df['Skills'].apply(lambda x: [s.strip().lower() for s in str(x).split(',')])
        mlb = MultiLabelBinarizer()
        skill_matrix = mlb.fit_transform(df['Skill_List'])
        y_salary = df['Salary (PKR)']
        y_worth = df['Worth_It'].apply(lambda x: 1 if str(x).strip().lower() == 'yes' else 0)
        
        reg = RandomForestRegressor(n_estimators=200, max_depth=12, random_state=42).fit(skill_matrix, y_salary)
        clf = RandomForestClassifier(n_estimators=200, random_state=42).fit(skill_matrix, y_worth)
        return mlb, reg, clf
    except Exception:
        return None, None, None


def parse_user_skills(user_input):
    return [s.strip().lower() for s in str(user_input).split(',') if s.strip()]


def classify_skills(field, user_skills):
    relevant_skills = ALL_FIELDS_DATA.get(field, [])
    show_relevant, show_gems, show_worst = [], [], []
    for skill in user_skills:
        if skill in relevant_skills:
            show_relevant.append(skill)
        elif skill in ALL_WORTHY_SKILLS:
            show_gems.append(skill)
        else:
            show_worst.append(skill)
    return show_relevant, show_gems, show_worst


def estimate_market_value(user_skills, mlb=None, salary_model=None, worth_model=None):
    salary = 0
    worth_status = 'NO'
    if not mlb or not salary_model or not worth_model:
        return salary, worth_status

    try:
        features = mlb.transform([user_skills])
        raw_salary = salary_model.predict(features)[0]
        valid_skills = [s for s in user_skills if s in ALL_WORTHY_SKILLS]
        salary = raw_salary + (len(valid_skills) * 4500)
        worth_status = 'YES' if worth_model.predict(features)[0] == 1 else 'NO'
    except Exception:
        pass
    return salary, worth_status


def skill_audit(field, user_input, csv_path='skilldata.csv'):
    user_skills = parse_user_skills(user_input)
    mlb, salary_model, worth_model = train_ml_engine(csv_path)
    salary, worth_status = estimate_market_value(user_skills, mlb, salary_model, worth_model)
    relevant, gems, volatile = classify_skills(field, user_skills)

    return {
        'field': field,
        'user_skills': user_skills,
        'estimated_salary_pkr': float(salary),
        'worth_status': worth_status,
        'field_assets': relevant,
        'cross_domain_gems': gems,
        'volatile_or_unknown': volatile,
    }