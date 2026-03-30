from fastapi import APIRouter
from pydantic import BaseModel
from groq import Groq

router = APIRouter()

class EmergencyInput(BaseModel):
    emergency_type: str
    country: str
    patient_age: str
    conscious: str
    situation: str
    api_key: str

@router.post("/firstaid")
def get_firstaid(data: EmergencyInput):
    try:
        client = Groq(api_key=data.api_key)
        prompt = f"""MEDICAL EMERGENCY - Immediate first aid needed.
        Emergency: {data.emergency_type}, Country: {data.country or 'Not specified'},
        Patient: {data.patient_age}, {data.conscious},
        Situation: {data.situation or 'Not described'}.
        Provide: Emergency number for {data.country},
        Step-by-step first aid (1-8 steps),
        Things to avoid, What to tell dispatcher.
        Be clear and life-saving.
        End with: This is first aid guidance only. Professional medical care is essential."""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=800,
            temperature=0.3
        )
        return {"instructions": response.choices[0].message.content}
    except Exception as e:
        return {"error": str(e)}
```

---

### File 14: `routers/__init__.py`

Create empty file `routers/__init__.py` — just leave it blank.

---

### File 15: `models/placeholder.txt`

Create `models/placeholder.txt` with content:
```
Upload rf_model.pkl, scaler.pkl and xray_model.onnx here