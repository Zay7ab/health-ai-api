from fastapi import APIRouter
from pydantic import BaseModel
from groq import Groq

router = APIRouter()

class BMIInput(BaseModel):
    height: float
    weight: float
    age: int
    gender: str
    activity: str
    goal: str
    systolic: int
    diastolic: int
    heart_rate: int
    api_key: str

@router.post("")
def calculate_bmi(data: BMIInput):
    try:
        height_m = data.height / 100
        bmi = data.weight / (height_m ** 2)

        if bmi < 18.5: bmi_status = "Underweight"
        elif bmi < 25: bmi_status = "Normal"
        elif bmi < 30: bmi_status = "Overweight"
        else: bmi_status = "Obese"

        if data.gender == "Male":
            bmr = 88.362 + (13.397 * data.weight) + (4.799 * data.height) - (5.677 * data.age)
            ideal_weight = 50 + 2.3 * ((data.height - 152.4) / 2.54)
        else:
            bmr = 447.593 + (9.247 * data.weight) + (3.098 * data.height) - (4.330 * data.age)
            ideal_weight = 45.5 + 2.3 * ((data.height - 152.4) / 2.54)

        multipliers = {
            "Sedentary (little/no exercise)": 1.2,
            "Lightly active (1-3 days/week)": 1.375,
            "Moderately active (3-5 days/week)": 1.55,
            "Very active (6-7 days/week)": 1.725,
            "Extra active (physical job)": 1.9
        }
        tdee = bmr * multipliers.get(data.activity, 1.2)

        if data.systolic < 120 and data.diastolic < 80: bp_status = "Normal"
        elif data.systolic < 130: bp_status = "Elevated"
        elif data.systolic < 140: bp_status = "High Stage 1"
        else: bp_status = "High Stage 2"

        # Get AI insight
        client = Groq(api_key=data.api_key)
        prompt = f"""Patient: BMI {bmi:.1f} ({bmi_status}), Age {data.age}, {data.gender},
        TDEE {tdee:.0f} kcal, Ideal weight {ideal_weight:.1f}kg (current {data.weight}kg),
        BP {data.systolic}/{data.diastolic} ({bp_status}), Goal: {data.goal}.
        Give a personalized 4-5 sentence health plan with diet and exercise recommendations.
        End with: Always consult a qualified doctor before starting any health program."""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300
        )

        return {
            "bmi": round(bmi, 1),
            "bmi_status": bmi_status,
            "bmr": round(bmr),
            "tdee": round(tdee),
            "ideal_weight": round(ideal_weight, 1),
            "bp_status": bp_status,
            "ai_insight": response.choices[0].message.content
        }
    except Exception as e:
        return {"error": str(e)}