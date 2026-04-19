import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def _get_client():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError('GROQ_API_KEY is missing.')
    return Groq(api_key=api_key)


def get_interview_seed_messages():
    return [
        {
            'role': 'assistant',
            'content': 'Welcome back, Hassan. System diagnostics complete. Enter your command to initiate the session.',
        }
    ]


def interview_challenge(user_input, history=None):
    if not user_input:
        raise ValueError('user_input is required')

    messages = list(history) if history else get_interview_seed_messages()
    messages.append({'role': 'user', 'content': user_input})

    client = _get_client()
    response = client.chat.completions.create(
        messages=[{'role': 'system', 'content': 'You are a highly sophisticated technical interviewer.'}] + messages,
        model='llama-3.3-70b-versatile',
    )
    reply = response.choices[0].message.content
    messages.append({'role': 'assistant', 'content': reply})

    return {
        'reply': reply,
        'messages': messages,
    }