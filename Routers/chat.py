from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional
from groq import Groq
import os

router = APIRouter()

class Message(BaseModel):
    role: str
    content: str

class ChatInput(BaseModel):
    message: str
    history: Optional[List[Message]] = []
    language: Optional[str] = "English"
    api_key: str

@router.post("")
def chat(data: ChatInput):
    try:
        client = Groq(api_key=data.api_key)

        system_prompt = f"""You are HealthAI Assistant — a professional, compassionate and highly 
        knowledgeable medical AI assistant. You respond in {data.language} language.
        - Analyze symptoms and suggest possible conditions
        - Provide evidence-based health information
        - Give medication information
        - Offer mental health support
        - Always recommend professional medical consultation
        - Never diagnose definitively
        Always end with: 'Please consult a qualified doctor for proper diagnosis.'"""

        messages = [{"role": "system", "content": system_prompt}]
        for msg in data.history:
            messages.append({"role": msg.role, "content": msg.content})
        messages.append({"role": "user", "content": data.message})

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.7,
            max_tokens=500
        )

        return {
            "reply": response.choices[0].message.content,
            "status": "success"
        }
    except Exception as e:
        return {"error": str(e)}