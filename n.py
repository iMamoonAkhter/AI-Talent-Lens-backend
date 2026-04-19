import pandas as pd
import random

# 1. Configuration
CITIES = ["Lahore", "Karachi", "Islamabad", "Faisalabad", "Peshawar", "Multan", "Quetta"]
STUDENT_NAMES = ["Ali", "Sara", "Ahmed", "Ayesha", "Usman", "Hina", "Bilal", "Fatima", "Zain", "Noor", "Hamza", "Mariam"]

# Skills mapping from your project
TOP_SKILLS = {
    "CS": {"Basics": ["python", "java", "c++", "dsa"], "Advanced": ["docker", "kubernetes", "react"]},
    "AI": {"Basics": ["python", "math", "ml"], "Advanced": ["deep learning", "nlp", "llms"]},
    "Data Science": {"Basics": ["python", "sql", "pandas"], "Advanced": ["big data", "deployment"]},
    "Cyber Security": {"Basics": ["networking", "linux"], "Advanced": ["ethical hacking", "cryptography"]},
    "Business Analytics": {"Basics": ["excel", "statistics"], "Advanced": ["power bi", "predictive modeling"]}
}

fields_list = list(TOP_SKILLS.keys())

# 2. Data Generation
data = []
for i in range(100):
    name = random.choice(STUDENT_NAMES)
    field = random.choice(fields_list)
    city = random.choice(CITIES)
    
    # Randomly pick skills (mixing basics and advanced)
    all_f_skills = TOP_SKILLS[field]["Basics"] + TOP_SKILLS[field]["Advanced"]
    selected_skills = random.sample(all_f_skills, k=random.randint(1, 3))
    
    # Salary Logic
    has_advanced = any(s in TOP_SKILLS[field]["Advanced"] for s in selected_skills)
    if has_advanced:
        salary = random.randint(120000, 350000)
    else:
        salary = random.randint(45000, 95000)
        
    # Worthit Logic (Must have at least 2 relevant skills)
    worthit = "Yes" if len(selected_skills) >= 2 else "No"
    
    data.append([name, field, ", ".join(selected_skills), city, salary, worthit])

# 3. Create DataFrame and Save
df = pd.DataFrame(data, columns=["name", "field", "skills", "city", "salary", "worthit"])

# Save to CSV
df.to_csv("skillscope_data.csv", index=False)

print("✅ 'skillscope_data.csv' with 100 rows has been created successfully!")
print(df.head())