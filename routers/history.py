from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from groq import Groq

router = APIRouter()

class HistoryRecord(BaseModel):
    Date: str
    Type: str
    Condition: str
    Doctor: str
    Medications: str
    Notes: str

class HistoryInput(BaseModel):
    records: List[HistoryRecord]
    api_key: str

@router.post("/analyze")
def analyze_history(data: HistoryInput):
    try:
        client = Groq(api_key=data.api_key)
        history_text = "\n".join([
            f"- {r.Date}: {r.Type} — {r.Condition} (Medications: {r.Medications or 'None'})"
            for r in data.records
        ])
        prompt = f"""Analyze this patient's medical history:\n{history_text}\n
        Provide: 1) Key health patterns, 2) Potential risks,
        3) Preventive measures, 4) Questions to ask doctor.
        End with: Always share your complete medical history with your doctor."""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=400
        )
        return {"analysis": response.choices[0].message.content}
    except Exception as e:
        return {"error": str(e)}