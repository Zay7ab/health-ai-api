from fastapi import APIRouter
from pydantic import BaseModel
from groq import Groq

router = APIRouter()

class ReportInput(BaseModel):
    name: str
    age: int
    gender: str
    bmi: float
    diagnosis: str
    symptoms: str
    medications: str
    heart_risk: str
    xray_result: str
    vitals: str
    api_key: str

@router.post("/notes")
def generate_notes(data: ReportInput):
    try:
        client = Groq(api_key=data.api_key)
        prompt = f"""Write professional doctor notes for:
        {data.name}, {data.age}yo {data.gender}, BMI {data.bmi:.1f},
        Diagnosis: {data.diagnosis or 'Not specified'},
        Symptoms: {data.symptoms or 'Not specified'},
        Medications: {data.medications or 'None'},
        Heart Risk: {data.heart_risk}, X-Ray: {data.xray_result},
        Vitals: {data.vitals or 'Not recorded'}.
        Write 3-4 sentences of formal clinical notes."""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=250
        )
        return {"notes": response.choices[0].message.content}
    except Exception as e:
        return {"error": str(e)}