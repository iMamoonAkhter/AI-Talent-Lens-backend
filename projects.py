from project_bot import build_project_chat_session


# --- DATA ---
TOP_SKILLS = {
    "CS": {"Basics": ["python", "java", "c++", "dsa"], "Advanced": ["docker", "react", "system design"]},
    "AI": {"Basics": ["python", "math", "statistics", "ml"], "Advanced": ["deep learning", "nlp", "llms"]},
    "Data Science": {"Basics": ["python", "sql", "pandas"], "Advanced": ["tableau", "big data", "deployment"]},
    "Cyber Security": {"Basics": ["networking", "linux"], "Advanced": ["ethical hacking", "cryptography"]},
    "SE": {"Basics": ["oop", "dsa", "testing"], "Advanced": ["agile", "devops", "ci/cd"]},
    "Business Analytics": {"Basics": ["excel", "sql"], "Advanced": ["power bi", "predictive modeling"]}
}

PROJECTS = {
    "CS": {
        "Easy": [
            ("Personal Portfolio", "A static website to showcase your resume and skills.", "HTML, CSS, JavaScript"),
            ("Basic Web Scraper", "Extract data from a simple website and save it to a file.", "Python, BeautifulSoup"),
            ("Inventory System", "A command-line tool to manage product stock.", "Python, JSON")
        ],
        "Medium": [
            ("Real-time Chat App", "A chat application using web sockets for instant messaging.", "React, Node.js, Socket.io"),
            ("E-commerce API", "A RESTful backend for a shopping cart system.", "Python, Flask, PostgreSQL"),
            ("Task Management Tool", "A Kanban-style board to track project progress.", "React, Firebase")
        ],
        "Hard": [
            ("Custom Compiler", "A mini-compiler for a subset of C language.", "C++, Flex, Bison"),
            ("Distributed Ledger", "A simple private blockchain implementation.", "Go, Cryptography"),
            ("Operating System Kernel", "A basic bootable kernel with memory management.", "C, Assembly, QEMU")
        ]
    },
    "AI": {
        "Easy": [
            ("Sentiment Analyzer", "Predict if a movie review is positive or negative.", "Python, Scikit-learn, NLTK"),
            ("Iris Flower Classifier", "The 'Hello World' of ML to classify flower species.", "Python, Pandas, ML"),
            ("Voice-to-Text Converter", "Convert spoken words into written text format.", "Python, SpeechRecognition API")
        ],
        "Medium": [
            ("Object Detection System", "Detect multiple objects in real-time video streams.", "Python, OpenCV, YOLO"),
            ("Music Recommendation", "Suggest songs based on user listening history.", "Python, Collaborative Filtering"),
            ("Stock Price Predictor", "Predict future prices using time-series analysis.", "Python, LSTM, Keras")
        ],
        "Hard": [
            ("Custom GPT Model", "Train a small-scale LLM on specific text data.", "PyTorch, Transformers, HuggingFace"),
            ("Self-Driving Car Simulation", "Teach a virtual car to drive using Reinforcement Learning.", "Python, Unity/Pygame, RL"),
            ("Medical Diagnosis AI", "Analyze X-ray images to detect anomalies or diseases.", "Deep Learning, CNN, TensorFlow")
        ]
    },
    "Data Science": {
        "Easy": [
            ("Titanic Survival Analysis", "EDA on passenger data to find survival patterns.", "Python, Seaborn, Matplotlib"),
            ("Sales Analysis Dashboard", "Clean and visualize monthly business sales.", "Excel, Power BI"),
            ("Weather Data Visualizer", "Pull weather data and plot temperature trends.", "Python, Plotly, API")
        ],
        "Medium": [
            ("Customer Churn Prediction", "Predict which customers are likely to leave a service.", "Python, XGBoost, Scikit-learn"),
            ("Credit Card Fraud Detection", "Identify fraudulent transactions in imbalanced data.", "Python, Random Forest, SMOTE"),
            ("Product Price Tracker", "Monitor and visualize price changes of online products.", "Python, SQL, Tableu")
        ],
        "Hard": [
            ("Big Data Supply Chain", "Analyze supply chain bottlenecks using large datasets.", "Apache Spark, Hadoop, Python"),
            ("Real-time Traffic Flow", "Predict urban traffic congestion using live sensor data.", "Kafka, Python, Streaming Analytics"),
            ("Financial Risk Engine", "Automated risk assessment for loan applications.", "Python, SQL, MLflow")
        ]
    },
    "Cyber Security": {
        "Easy": [
            ("Network Port Scanner", "Check for open and vulnerable ports on a network.", "Python, Nmap"),
            ("Simple File Encryptor", "Encrypt and decrypt text files using AES.", "Python, Cryptography library"),
            ("Password Manager", "Store passwords securely with master-key access.", "Python, SQLite, Hashlib")
        ],
        "Medium": [
            ("Intrusion Detection System", "Monitor network logs for suspicious activities.", "Snort, Python, Linux"),
            ("SQL Injection Lab", "A safe environment to practice and prevent SQLi attacks.", "PHP, MySQL, Docker"),
            ("Packet Sniffer", "Capture and analyze network packets in real-time.", "Python, Scapy, Wireshark")
        ],
        "Hard": [
            ("Malware Analysis Sandbox", "A secure environment to execute and monitor malware.", "Cuckoo Sandbox, VirtualBox"),
            ("Ethical Hacking Framework", "Automate reconnaissance and exploitation tasks.", "Metasploit, Python, Kali Linux"),
            ("Zero-Trust Architecture", "Implement a zero-trust model for a small office network.", "Firewalls, VPN, MFA")
        ]
    },
    "SE": {
        "Easy": [
            ("Unit Testing Suite", "Write automated tests for an existing application.", "Python, Pytest"),
            ("Documentation Generator", "Convert code comments into professional docs.", "Sphinx, Markdown"),
            ("Bug Tracker", "A simple system to report and manage software bugs.", "Java, Spring Boot")
        ],
        "Medium": [
            ("CI/CD Pipeline", "Automate build, test, and deployment for a project.", "Jenkins, Docker, GitHub Actions"),
            ("Microservices App", "A weather app split into multiple small services.", "Node.js, Docker, Kubernetes"),
            ("Social Media Backend", "Design the logic for followers, likes, and posts.", "Go, MongoDB, Redis")
        ],
        "Hard": [
            ("Scalable Streaming App", "A Netflix clone designed for high availability.", "AWS, Kafka, React"),
            ("System Monitor Tool", "Real-time monitoring of CPU, RAM, and Server health.", "Prometheus, Grafana, Go"),
            ("DevOps Automation Hub", "Tool to automate cloud infrastructure setup.", "Terraform, Ansible, Python")
        ]
    },
    "Business Analytics": {
        "Easy": [
            ("Marketing Campaign ROI", "Calculate the profit from a marketing budget.", "Excel, SQL"),
            ("Inventory Audit Report", "Find discrepancies in stock data using formulas.", "Excel, VBA"),
            ("Customer Feedback Survey", "Visualize survey results for business insights.", "Google Forms, Power BI")
        ],
        "Medium": [
            ("Retail Sales Forecasting", "Predict next month's sales using historical data.", "Python, SQL, Tableau"),
            ("Employee Attrition Analysis", "Find reasons why employees are leaving.", "Python, HR Analytics"),
            ("E-commerce Funnel", "Track user journey from home page to purchase.", "Google Analytics, SQL")
        ],
        "Hard": [
            ("Price Optimization Model", "Find the best price point to maximize profit.", "Python, Optimization algorithms"),
            ("Dynamic Supply Chain Dashboard", "Real-time tracking of logistics and costs.", "Power BI, Azure, SQL"),
            ("Sentiment-Based Strategy", "Analyze Twitter data to guide business decisions.", "NLP, Python, Power BI")
        ]
    }
}



def get_fields():
    return list(TOP_SKILLS.keys())


def get_required_skills(field):
    skills = TOP_SKILLS.get(field, {})
    return {
        'basics': list(skills.get('Basics', [])),
        'advanced': list(skills.get('Advanced', [])),
    }


def get_projects(field, level):
    return [
        {
            'name': name,
            'description': desc,
            'tech_stack': tools,
        }
        for name, desc, tools in PROJECTS.get(field, {}).get(level, [])
    ]


def build_project_recommendation(field, level='Easy'):
    return {
        'field': field,
        'level': level,
        'skills': get_required_skills(field),
        'projects': get_projects(field, level),
    }


def get_project_chat_response(user_input, history=None):
    return build_project_chat_session(user_input=user_input, history=history)