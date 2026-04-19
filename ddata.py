FIELDS = ["CS", "IT", "MBBS", "BBA", "BA", "SE", "AI", "Data Science", "Cyber Security", "Business Analytics"]
CITIES = ["Lahore", "Karachi", "Islamabad", "Faisalabad", "Peshawar", "Multan", "Quetta"]

FIELD_ALIASES = {f.lower(): f for f in FIELDS}
FIELD_ALIASES.update({"computer science": "CS", "software engineering": "SE", "data": "Data Science", "cyber": "Cyber Security"})

TOP_SKILLS = {
    "CS": {
        "Basics": ["python", "java", "c++", "dsa"],
        "Advanced": ["docker", "react", "system design"]
    },

    "AI": {
        "Basics": ["python", "math", "statistics", "ml"],
        "Advanced": ["deep learning", "nlp", "llms"]
    },

    "Data Science": {
        "Basics": ["python", "sql", "pandas"],
        "Advanced": ["tableau", "big data", "deployment"]
    },

    "Cyber Security": {
        "Basics": ["networking", "linux"],
        "Advanced": ["ethical hacking", "cryptography"]
    },

    "SE": {
        "Basics": ["oop", "dsa", "testing"],
        "Advanced": ["agile", "devops", "ci/cd"]
    },

    "Business Analytics": {
        "Basics": ["excel", "sql"],
        "Advanced": ["power bi", "predictive modeling"]
    },

    # ✅ NEW ADDITIONS
    "IT": {
        "Basics": [
            "networking", 
            "hardware", 
            "operating systems"
        ],
        "Advanced": [
            "cloud computing", 
            "system administration", 
            "security"
        ]
    },

    "MBBS": {
        "Basics": [
            "anatomy", 
            "physiology", 
            "biochemistry"
        ],
        "Advanced": [
            "clinical practice", 
            "surgery", 
            "diagnosis"
        ]
    },

    "BBA": {
        "Basics": [
            "management", 
            "marketing", 
            "business communication"
        ],
        "Advanced": [
            "strategic management", 
            "finance", 
            "entrepreneurship"
        ]
    },

    "BA": {
        "Basics": [
            "communication", 
            "writing", 
            "critical thinking"
        ],
        "Advanced": [
            "research", 
            "analysis", 
            "public speaking"
        ]
    }

    # 🔥 OPTIONAL BUT RECOMMENDED (since you already had IT earlier)

    
}



LEARNING_LINKS = {
    "python": "https://www.youtube.com/watch?v=UrsmFxEIp5k",
    "java": "https://www.youtube.com/watch?v=eIrMbAQSU34",
    "c++": "https://www.youtube.com/watch?v=e7sAf4SbS_g",
    "dsa": "https://www.youtube.com/watch?v=QwSgyhSAJnc&t=341s",
    "oop": "https://www.youtube.com/watch?v=Mf2RdpEiXjU&t=3370s",
    "react": "https://www.youtube.com/watch?v=3LRZRSIh_KE",
    "ml": "https://www.youtube.com/watch?v=LvC68w9JS4Y&t=51s",
    "statistics": "https://www.youtube.com/watch?v=bLZ-LSsQMCc&t=5944s",
    "sql": "https://www.youtube.com/watch?v=hlGoQC332VM",
    "pandas": "https://www.youtube.com/watch?v=vtgDGrUiUKk",
    "networking": "https://www.youtube.com/watch?v=IPvYjXCsTg8",
    "linux": "https://www.youtube.com/watch?v=iwolPf6kN-k",
    
    
    "anatomy": "https://www.youtube.com/watch?v=o707an6kcvE",
    "physiology": "https://www.youtube.com/watch?v=Ki21TpGDx9g",
    "biochemistry": "https://www.youtube.com/watch?v=eJqpYly2hvY",
    "surgery": "https://www.youtube.com/watch?v=PwmEddQ9jMM",
    "diagnosis": "https://www.youtube.com/watch?v=_KSSf1NtZkE",

    "management": "https://www.youtube.com/watch?v=uWPIsaYpY7U",
    "marketing": "https://www.youtube.com/watch?v=XuUbLHIRyuM",
    "finance": "https://www.youtube.com/watch?v=AkMTxMN7res",
    "entrepreneurship": "https://www.youtube.com/watch?v=A6BktbsRPr4",

    "communication": "https://www.youtube.com/watch?v=-FIcgjCHR_o",
    "writing": "https://www.youtube.com/watch?v=wDhU9fOAhiA",
    "critical thinking": "https://www.youtube.com/watch?v=tOFPtiM48qg",
    "research": "https://www.youtube.com/watch?v=ZpwZS3XnEZA",

    "cloud computing": "https://www.youtube.com/watch?v=EN4fEbcFZ_E",
    "system administration": "https://www.youtube.com/watch?v=m8Icp_Cid5o",
    "security": "https://www.youtube.com/watch?v=v3iUx2SNspY&t=3407s",
    "docker":"https://www.youtube.com/watch?v=pTFZFxd4hOI",
    "system design":"https://www.youtube.com/watch?v=m8Icp_Cid5o&t=16s",
    "hardware":"https://www.youtube.com/watch?v=DgmAwSE-H10&list=PLmbkTCZhP_q8VL090roDdHkwl_ft7dKdl",
    "operating systems":"https://www.youtube.com/watch?v=yK1uBHPdp30",
    "clinical practice":"https://www.youtube.com/watch?v=yJNUq7bih8c",
    "business communication":"https://www.youtube.com/watch?v=DnWOFf1WxTs",
    "strategic management":"https://www.youtube.com/watch?v=EJHPltmAULA",
    "analysis":"https://www.youtube.com/watch?v=YW3A5deSxiA",
    "public speaking":"https://www.youtube.com/watch?v=MXKkXXYUxBc",
    "agile":"https://www.youtube.com/watch?v=QvhPNI5WkD0",
    "testing":"https://www.youtube.com/watch?v=P31bOYX1lZE&list=PLwbMf8x0S9vBcE3i5qtf0BrqXS9OZ1LXR",
    "ci/cd":"https://www.youtube.com/watch?v=h9K1NnqwUvE",
    "devops":"https://www.youtube.com/watch?v=9-psq7Uwa3Q&list=PL5OhSdfH4uDsyUM02ZHl2mOYBpihCYsml",
    "deep learning":"https://www.youtube.com/watch?v=VyWAvY2CF9c&t=5115s",
    "nlp":"https://www.youtube.com/watch?v=-33oXx0TwHI",
    "llms":"https://www.youtube.com/watch?v=p3sij8QzONQ",
    "tableau":"https://www.youtube.com/watch?v=GbszEsOY3wo",
    "big data":"https://www.youtube.com/watch?v=OP8BsGnqi9c",
    "deployment":"https://www.youtube.com/watch?v=vzVbqXVID-Y",
    "ethical hacking":"https://www.youtube.com/watch?v=ug8W0sFiVJo",
    "cryptography":"https://www.youtube.com/watch?v=kb_scuDUHls",
    "power bi":"https://www.youtube.com/watch?v=FwjaHCVNBWA",
    "predictive modeling":"https://www.youtube.com/watch?v=zZwunHv3Zog"
}

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


FIELD_BG = {
    "AI": "images/ai.jpg",
    "CS": "images/cs.jpg",
    "Data Science": "images/ds.jpg",
    "Cyber Security": "images/cyber.jpg",
    "SE": "images/se.jpg",
    "Business Analytics": "images/busines.jpg",
    "MBBS": "images/mbbs.jpg",
    "BBA": "images/bba.jpg",
    "BA": "images/ba.jpg",
    "IT": "images/it.jpg"
}