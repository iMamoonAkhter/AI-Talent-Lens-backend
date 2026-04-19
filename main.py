import os
import tempfile
from typing import List, Optional, Literal

from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from ml import (
    FIELDS as RESUME_FIELDS,
    extract_text,
    extract_skills,
    extract_education,
    extract_experience,
    match_field,
    skill_gap,
    calculate_score,
)


class ChatMessage(BaseModel):
    role: Literal["system", "user", "assistant"]
    content: str = Field(..., min_length=1)


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1)
    history: List[ChatMessage] = Field(default_factory=list)


class ChatResponse(BaseModel):
    success: bool
    messages: List[ChatMessage]
    error: Optional[str] = None


app = FastAPI(title="Project Chat API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/resume-fields")
def resume_fields():
    return {"fields": list(RESUME_FIELDS.keys())}


@app.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest):
    if not os.environ.get("GROQ_API_KEY"):
        raise HTTPException(
            status_code=500,
            detail="GROQ_API_KEY is missing. Set it in your environment before calling /chat.",
        )

    history_payload = [msg.model_dump() for msg in payload.history]

    try:
        from project_bot import build_project_chat_session
        result = build_project_chat_session(user_input=payload.message, history=history_payload)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Groq API request failed: {str(exc)}") from exc

    messages_raw = result.get("messages", [])
    messages = [
        ChatMessage(**msg)
        for msg in messages_raw
        if isinstance(msg, dict) and msg.get("role") and msg.get("content")
    ]

    if result.get("error"):
        return ChatResponse(success=False, messages=messages, error=result["error"])

    return ChatResponse(success=True, messages=messages)


@app.post("/analyze-resume")
async def analyze_resume(file: UploadFile = File(...), field: str = Form(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="A PDF file is required.")

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    selected_field = next(
        (field_name for field_name in RESUME_FIELDS.keys() if field_name.lower() == field.lower().strip()),
        None,
    )
    if not selected_field:
        raise HTTPException(status_code=400, detail=f"Field '{field}' is not supported.")

    temp_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            content = await file.read()
            if not content:
                raise HTTPException(status_code=400, detail="Uploaded file is empty.")
            temp_file.write(content)
            temp_path = temp_file.name

        extracted_text = extract_text(temp_path)
        user_skills = extract_skills(extracted_text)
        education = extract_education(extracted_text)
        experience = extract_experience(extracted_text)

        detected_field, _ = match_field(user_skills)
        score = calculate_score(user_skills, selected_field)
        missing_skills = skill_gap(user_skills, selected_field)

        suggestions = [f"Add or improve: {skill}" for skill in missing_skills[:8]]
        if score < 50:
            suggestions.append("Focus on foundational projects and certifications in your matched field.")
        elif score < 75:
            suggestions.append("Strengthen advanced tools and add measurable project outcomes.")
        else:
            suggestions.append("Great profile. Prioritize portfolio polish and interview readiness.")

        return {
            "success": True,
            "skills": user_skills,
            "education": education,
            "experience": experience,
            "field": selected_field,
            "detected_field": detected_field,
            "score": score,
            "missing_skills": missing_skills,
            "suggestions": suggestions,
        }
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Resume analysis failed: {str(exc)}") from exc
    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)


def run_skill_bot(module_name, **kwargs):
    module = (module_name or '').strip().lower()

    if module == 'market':
        from assesment import skill_audit
        return skill_audit(
            field=kwargs.get('field', 'CS'),
            user_input=kwargs.get('user_input', ''),
            csv_path=kwargs.get('csv_path', 'skilldata.csv'),
        )

    if module == 'projects':
        from projects import build_project_recommendation
        return build_project_recommendation(
            field=kwargs.get('field', 'CS'),
            level=kwargs.get('level', 'Easy'),
        )

    if module == 'project_chat':
        from projects import get_project_chat_response
        return get_project_chat_response(
            user_input=kwargs.get('user_input', ''),
            history=kwargs.get('history'),
        )

    if module == 'roadmap':
        from roadmap import recommend_fields_and_skills
        return recommend_fields_and_skills(
            name=kwargs.get('name', ''),
            choice=kwargs.get('choice', ''),
        )

    if module == 'interview':
        from skill_chatbot import interview_challenge
        return interview_challenge(
            user_input=kwargs.get('user_input', ''),
            history=kwargs.get('history'),
        )

    if module == 'powerbi':
        from powerbi import show_powerbi_insights
        return show_powerbi_insights()

    raise ValueError(
        'Unknown module_name. Use one of: market, projects, project_chat, roadmap, interview, powerbi'
    )