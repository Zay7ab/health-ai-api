from fastapi import APIRouter
from pydantic import BaseModel
from groq import Groq

router = APIRouter()

class RiskInput(BaseModel):
    age: int
    smoking: str
    diabetes: str
    bp: str
    cholesterol: str
    exercise: str
    family_history: str
    obesity: str
    stress: str
    api_key: str

@router.post("")
def calculate_risk(data: RiskInput):
    try:
        score = 0
        factors = {}

        if data.age > 55: score += 25; factors["Age"] = "High Risk"
        elif data.age > 45: score += 15; factors["Age"] = "Moderate"
        else: factors["Age"] = "Low Risk"

        if data.smoking == "Current": score += 25; factors["Smoking"] = "Current Smoker"
        elif data.smoking == "Former": score += 10; factors["Smoking"] = "Former Smoker"
        else: factors["Smoking"] = "Non-Smoker"

        if data.diabetes == "Yes": score += 15; factors["Diabetes"] = "Diabetic"
        else: factors["Diabetes"] = "No Diabetes"

        if data.bp == "Yes": score += 15; factors["Blood Pressure"] = "High BP"
        else: factors["Blood Pressure"] = "Normal BP"

        if data.cholesterol == "Yes": score += 10; factors["Cholesterol"] = "High"
        else: factors["Cholesterol"] = "Normal"

        if data.exercise == "No": score += 10; factors["Exercise"] = "Inactive"
        else: factors["Exercise"] = "Active"

        if data.family_history == "Yes": score += 10; factors["Family History"] = "Present"
        else: factors["Family History"] = "None"

        if data.obesity == "Yes": score += 10; factors["Obesity"] = "Obese"
        else: factors["Obesity"] = "Normal"

        if data.stress == "Yes": score += 5; factors["Stress"] = "High"
        else: factors["Stress"] = "Low"

        score = min(score, 100)

        if score < 20: risk_level = "Low Risk"
        elif score < 40: risk_level = "Moderate Risk"
        elif score < 65: risk_level = "High Risk"
        else: risk_level = "Very High Risk"

        client = Groq(api_key=data.api_key)
        active_risks = [k for k, v in factors.items() if "High" in v or "Current" in v or "Diabetic" in v]
        prompt = f"""Cardiovascular risk: {score}% ({risk_level}), Age: {data.age},
        Key risks: {', '.join(active_risks) if active_risks else 'None'}.
        Give 4-5 sentence personalized prevention plan.
        End with: Consult a cardiologist for comprehensive evaluation."""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300
        )

        return {
            "score": score,
            "risk_level": risk_level,
            "factors": factors,
            "ai_plan": response.choices[0].message.content
        }
    except Exception as e:
        return {"error": str(e)}