from fastapi import APIRouter
from pydantic import BaseModel
from groq import Groq

router = APIRouter()

class TipsInput(BaseModel):
    category: str
    age_group: str
    api_key: str

class DailyTipInput(BaseModel):
    api_key: str

@router.post("/generate")
def generate_tips(data: TipsInput):
    try:
        client = Groq(api_key=data.api_key)
        prompt = f"""Generate 5 specific actionable health tips about {data.category}
        for someone aged {data.age_group}.
        Format each as:
        TITLE: [short title max 5 words]
        TIP: [2-3 sentence detailed explanation]
        Number them 1-5."""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=600
        )
        return {"tips": response.choices[0].message.content}
    except Exception as e:
        return {"error": str(e)}

@router.post("/daily")
def daily_tip(data: DailyTipInput):
    try:
        client = Groq(api_key=data.api_key)
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": "Give one powerful health tip in 2 sentences. Be specific and actionable. No intro."}],
            max_tokens=80
        )
        return {"tip": response.choices[0].message.content}
    except Exception as e:
        return {"error": str(e)}