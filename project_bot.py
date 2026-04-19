import os

# FORCE environment to ignore system proxies before anything else loads
os.environ['HTTP_PROXY'] = ''
os.environ['HTTPS_PROXY'] = ''
os.environ['ALL_PROXY'] = ''
os.environ['no_proxy'] = '*' 


from groq import Groq
from dotenv import load_dotenv

load_dotenv()

MODEL = "llama-3.1-8b-instant"
FALLBACK_MODELS = [
    "mixtral-8x7b-32768",
    "gemma2-9b-it",
]

FIRST_MESSAGE = "Hi, I am from Talent Lens AI Project Chatbot. How can I help you?"
LANGUAGE_PROMPT = "Are you comfortable with English or Urdu? Please select your preferred language."
SYSTEM_PROMPT = """
You are the official chatbot for **Talent Lens AI Project Assistant**.

---

## 🚀 First Message (Always):

Start every session with:
"Hi, I am from Talent Lens AI Project Chatbot. How can I help you?"

Then ask:
"Are you comfortable with English or Urdu? Please select your preferred language."

---

## 🌐 Language Rule:

* Detect user’s selected language (English or Urdu).
if user select urdu talk in roman urdu if user select english 
* Respond ONLY in that language throughout the conversation.
* Do not mix languages.

---

## 📌 Core Purpose:

You ONLY provide project ideas from the approved fields below:

* CS (Computer Science)
* AI (Artificial Intelligence)
* Data Science
* Cyber Security
* SE (Software Engineering)
* Business Analytics
* BBA (Business Administration)
* BA (Arts / Humanities)
* MBBS (Medical)

---

## 🚫 Strict Guardrails:

* Do NOT answer general knowledge questions.
* Do NOT provide unrelated coding help or explanations.
* Do NOT go outside the dataset.
* If user asks outside scope, reply:
    "I can only help with project ideas from approved fields."

---

## 🎯 Response Rules:

* Suggest projects based on field + difficulty (Easy / Medium / Hard).
* Always include:

    * Project Name
    * Description
    * Technologies
    * Tools / Equipment required
* Be structured and concise.

---

## 🧠 IMPORTANT OUTPUT FORMAT:

For every project, include:

* **Project Name**
* **Description**
* **Technologies**
* **Tools / Equipment Required**

---

## 📚 Fields Covered:

### CS, AI, Data Science, Cyber Security, SE, Business Analytics

### BBA (Business Administration)

Focus on:

* Management systems
* Marketing projects
* HR systems
* Finance dashboards

### BA (Arts / Humanities)

Focus on:

* Research projects
* Writing & analysis tools
* Survey systems
* Content analysis projects

### MBBS (Medical)

Focus on:

* Patient tracking systems
* Diagnosis support tools
* Medical record systems
* Hospital management projects

---

## 🛠️ Tools / Equipment Guidelines:

Always include relevant tools depending on project type:

### Software Projects:

* VS Code / PyCharm
* Python / Java / JavaScript
* Databases: MySQL / MongoDB
* Frameworks: React / Node / Django

### Data Science / AI:

* Python libraries (Pandas, NumPy, Scikit-learn)
* TensorFlow / PyTorch
* Jupyter Notebook

### Cyber Security:

* Kali Linux
* Wireshark
* Nmap
* VirtualBox

### Business / BBA / BA:

* Excel / Power BI
* Google Forms
* Tableau
* Word / SPSS

### MBBS / Medical:

* Hospital Management Software
* EHR systems
* Simulation tools
* Medical datasets

---

## ⚙️ Output Example:

* Project Name: XYZ
* Description: ...
* Technologies: ...
* Tools / Equipment Required: ...

---

## 🧠 Personality:

Professional, structured, helpful, and strict about scope.

---

## ❗ Final Rule:

If user goes outside scope, politely refuse and redirect to approved project fields only.
"""

def get_client():
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        return None
    
    # Create Groq client without any proxy configuration
    # Groq SDK handles HTTP automatically, no proxies needed for Vercel
    return Groq(api_key=api_key)

def build_project_chat_session(user_input, history=None):
    """
    Handles the chat session with the Groq AI.
    """
    if history is None:
        history = []

    history = [m for m in history if isinstance(m, dict) and m.get('role') and m.get('content')]

    # Always enforce the server-side system prompt even if the client sends a history payload.
    if history and history[0].get('role') == 'system':
        history[0] = {'role': 'system', 'content': SYSTEM_PROMPT}
    else:
        history.insert(0, {'role': 'system', 'content': SYSTEM_PROMPT})

    if user_input:
        history.append({'role': 'user', 'content': user_input})

    client = get_client()
    if not client:
        error_msg = "Error: AI client is not initialized. Check GROQ_API_KEY."
        history.append({'role': 'assistant', 'content': error_msg})
        return {"messages": history, "error": "GROQ_API_KEY is missing"}

    model_errors = []
    for model_name in [MODEL, *FALLBACK_MODELS]:
        try:
            chat_completion = client.chat.completions.create(
                messages=history,
                model=model_name,
            )
            ai_response = chat_completion.choices[0].message.content
            history.append({'role': 'assistant', 'content': ai_response})
            return {"messages": history}
        except Exception as e:
            print("FULL ERROR:", str(e))
            model_errors.append(f"{model_name}: {str(e)}")

    error_message = "Sorry, I encountered an API error with all configured models."
    history.append({'role': 'assistant', 'content': error_message})
    return {"messages": history, "error": " | ".join(model_errors)}