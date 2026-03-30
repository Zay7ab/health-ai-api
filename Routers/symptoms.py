from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from groq import Groq

router = APIRouter()

class SymptomsInput(BaseModel):
    age: int
    gender: str
    symptoms: List[str]
    duration: str
    severity: str
    existing_conditions: List[str]
    medications: str
    additional: str
    api_key: str

@router.post("/check")
def check_symptoms(data: SymptomsInput):
    try:
        client = Groq(api_key=data.api_key)
        prompt = f"""Patient: Age {data.age}, {data.gender},
        Symptoms: {', '.join(data.symptoms)},
        Duration: {data.duration}, Severity: {data.severity},
        Existing: {', '.join(data.existing_conditions)},
        Medications: {data.medications or 'None'},
        Additional: {data.additional or 'None'}.
        Provide: Top 3 possible conditions with urgency, red flags, next steps.
        End with: This is not a medical diagnosis. Please consult a qualified doctor."""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=600
        )

        is_urgent = (data.severity in ["Severe", "Very Severe"] or
                    "Chest Pain" in data.symptoms or
                    "Shortness of Breath" in data.symptoms)

        return {
            "analysis": response.choices[0].message.content,
            "is_urgent": is_urgent,
            "symptoms_count": len(data.symptoms)
        }
    except Exception as e:
        return {"error": str(e)}