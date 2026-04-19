from ddata import FIELDS, TOP_SKILLS, FIELD_ALIASES, LEARNING_LINKS
from road_data import CS_ROADMAP_3_MONTHS, AI_ROADMAP_3_MONTHS, DATA_SCIENCE, CYBER_SECURITY, SOFTWARE_ENGINEERING, BUSINESS_ANALYTICS, MBBS, BBA, BA, IT

# --- JOB SUGGESTIONS ---
JOB_ROLES = {
    "CS": ["Software Engineer", "Backend Developer", "Frontend Developer"],
    "AI": ["ML Engineer", "AI Engineer", "Data Scientist"],
    "Data Science": ["Data Analyst", "Data Scientist", "BI Analyst"],
    "Cyber Security": ["Security Analyst", "Penetration Tester", "SOC Analyst"],
    "SE": ["Software Engineer", "QA Engineer", "DevOps Engineer"],
    "Business Analytics": ["Business Analyst", "Data Analyst"],
    "MBBS": ["Doctor", "Surgeon", "Medical Officer"],
    "BBA": ["Business Manager", "Marketing Manager", "HR Manager"],
    "BA": ["Content Writer", "Research Analyst", "Public Relations Officer"],
    "IT": ["System Admin", "Network Engineer", "Cloud Engineer"]
}

def get_skill_score(level):
    if level == 'Advanced':
        return '⭐⭐⭐⭐⭐'
    if level == 'Basics':
        return '⭐⭐⭐'
    return '⭐⭐'


ROADMAP_MAP = {
    'CS': CS_ROADMAP_3_MONTHS,
    'AI': AI_ROADMAP_3_MONTHS,
    'Data Science': DATA_SCIENCE,
    'Cyber Security': CYBER_SECURITY,
    'SE': SOFTWARE_ENGINEERING,
    'Business Analytics': BUSINESS_ANALYTICS,
    'MBBS': MBBS,
    'BBA': BBA,
    'BA': BA,
    'IT': IT,
}


def normalize_field_key(field_key):
    normalized_key = field_key.strip()
    lowered = normalized_key.lower()
    if lowered in ['computer science', 'cs']:
        return 'CS'
    if lowered in ['artificial intelligence', 'ai']:
        return 'AI'
    if lowered in ['data science', 'ds']:
        return 'Data Science'
    if lowered in ['cyber security', 'cybersecurity']:
        return 'Cyber Security'
    if lowered in ['software engineering', 'se']:
        return 'SE'
    if lowered in ['business analytics']:
        return 'Business Analytics'
    if lowered in ['it']:
        return 'IT'
    return normalized_key


def _skill_entry(skill, level):
    return {
        'name': skill,
        'score': get_skill_score(level),
        'resource': LEARNING_LINKS.get(skill.lower(), 'https://google.com'),
        'level': level,
    }


def recommend_fields_and_skills(name, choice):
    if not name or not choice:
        raise ValueError('name and choice are required')

    field_key = FIELD_ALIASES.get(choice.lower(), choice)
    normalized_key = normalize_field_key(field_key)

    roadmap = TOP_SKILLS.get(field_key, {
        'Basics': ['Fundamentals'],
        'Advanced': ['Expert Projects'],
    })
    basics = roadmap.get('Basics', [])
    advanced = roadmap.get('Advanced', [])

    selected_roadmap = ROADMAP_MAP.get(normalized_key, {})
    jobs = JOB_ROLES.get(field_key, ['Specialist', 'Consultant'])

    return {
        'name': name.upper(),
        'choice': choice,
        'field_key': field_key,
        'normalized_key': normalized_key,
        'available_fields': list(FIELDS),
        'jobs': jobs,
        'core_competencies_count': len(basics),
        'advanced_assets_count': len(advanced),
        'foundation_layer': [_skill_entry(skill, 'Basics') for skill in basics],
        'specialist_layer': [_skill_entry(skill, 'Advanced') for skill in advanced],
        'deployment_schedule': selected_roadmap,
    }