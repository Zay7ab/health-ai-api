from fastapi import APIRouter
from pydantic import BaseModel
from groq import Groq

router = APIRouter()

class DoctorInput(BaseModel):
    condition: str
    city: str
    specialty: str
    urgency: str
    budget: str
    insurance: str
    language: str
    additional: str
    api_key: str

@router.post("/find")
def find_doctor(data: DoctorInput):
    try:
        client = Groq(api_key=data.api_key)
        prompt = f"""Find best doctors and hospitals for:
        Condition: {data.condition}, Location: {data.city},
        Specialty: {data.specialty}, Urgency: {data.urgency},
        Budget: {data.budget}, Insurance: {data.insurance},
        Language: {data.language or 'Any'},
        Requirements: {data.additional or 'None'}.
        Provide: Specialist type, Top 3 doctors, Top 3 hospitals,
        Preparation checklist, Red flags.
        End with: Always verify doctor credentials before booking."""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000
        )
        return {"recommendations": response.choices[0].message.content}
    except Exception as e:
        return {"error": str(e)}