from fastapi import APIRouter
from pydantic import BaseModel
import joblib
import numpy as np
import os

router = APIRouter()

# Load models
model_path = os.path.join(os.path.dirname(__file__), '..', 'models', 'rf_model.pkl')
scaler_path = os.path.join(os.path.dirname(__file__), '..', 'models', 'scaler.pkl')

try:
    rf_model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    print("✅ Heart models loaded!")
except Exception as e:
    print(f"❌ Heart model error: {e}")
    rf_model = None
    scaler = None

class HeartInput(BaseModel):
    id: float
    age: float
    sex: int
    dataset: int
    cp: int
    trestbps: float
    chol: float
    fbs: int
    restecg: int
    thalach: float
    exang: int
    oldpeak: float
    slope: int
    ca: int
    thal: int

@router.post("/heart")
def predict_heart(data: HeartInput):
    try:
        if rf_model is None:
            return {"error": "Model not loaded"}

        input_data = np.array([[
            data.id, data.age, data.sex, data.dataset,
            data.cp, data.trestbps, data.chol, data.fbs,
            data.restecg, data.thalach, data.exang,
            data.oldpeak, data.slope, data.ca, data.thal
        ]])

        input_scaled = scaler.transform(input_data)
        prediction = rf_model.predict(input_scaled)[0]
        probability = rf_model.predict_proba(input_scaled)[0][1]

        return {
            "prediction": int(prediction),
            "probability": float(probability),
            "risk_level": "High Risk" if prediction == 1 else "Low Risk",
            "probability_percent": f"{probability*100:.1f}%"
        }
    except Exception as e:
        return {"error": str(e)}