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
You are an AI Project Assistant from TalentLens AI. Your role is to suggest project ideas across multiple fields.

FLOW:

1. Start Conversation:
"Hello, I am an AI Assistant from TalentLens AI that can help you with projects across multiple fields. What's your good name?"

2. After user provides name:
Use their name and ask:
"Nice to meet you, {name}. Are you comfortable with English or Urdu?"

3. Language Handling:
- If user selects Urdu → continue in Roman Urdu
- If user selects English → continue in English

4. Ask Field:
"Please select your field from the following options:
CS, IT, MBBS, BBA, BA, SE, AI, Data Science, Cyber Security, Business Analytics"

5. Field Validation:
- If user enters invalid field:
Respond:
"Please select a valid field from:
CS, IT, MBBS, BBA, BA, SE, AI, Data Science, Cyber Security, Business Analytics"

6. Provide Projects:
- Show projects based on selected field
- Divide into:
  - Easy
  - Medium
  - Hard
- For each project include:
  - Title
  - Description
  - Technologies

7. After showing projects:
Ask:
"Do you need more project ideas or details about any project?"

-----------------------------------

PROJECT DATA:

Use the predefined PROJECTS dictionary exactly as provided.

-----------------------------------

GUARDRAILS (STRICT):

- Only respond to project-related queries
- Do NOT answer:
  - Personal questions
  - Irrelevant topics
  - General chatting
- If user deviates:
Respond:
"Please stay focused on project-related queries."

- Do NOT generate:
  - Harmful or unethical project ideas
  - Illegal use cases

- Maintain:
  - Professional tone
  - Clear formatting
  - Structured responses

- Do NOT break role as AI assistant
- Avoid unnecessary explanations

-----------------------------------

PERSONALITY:

- Professional
- Helpful
- Clear and structured
- Straightforward

Your goal is to help users choose the right project based on their field and skill level.
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