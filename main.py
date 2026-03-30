from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sys
import os

# Add app directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

app = FastAPI(
    title="HealthAI API",
    description="AI-Powered Health Prediction & Analysis API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import routers after path fix
from routers import heart, xray, chat, bmi, risk, symptoms, tips, history, report, doctor, emergency

app.include_router(heart.router, prefix="/predict", tags=["Heart Disease"])
app.include_router(xray.router, prefix="/predict", tags=["X-Ray Analysis"])
app.include_router(chat.router, prefix="/chat", tags=["Chatbot"])
app.include_router(bmi.router, prefix="/bmi", tags=["BMI Calculator"])
app.include_router(risk.router, prefix="/risk", tags=["Risk Gauge"])
app.include_router(symptoms.router, prefix="/symptoms", tags=["Symptom Checker"])
app.include_router(tips.router, prefix="/tips", tags=["Health Tips"])
app.include_router(history.router, prefix="/history", tags=["Medical History"])
app.include_router(report.router, prefix="/report", tags=["Patient Report"])
app.include_router(doctor.router, prefix="/doctor", tags=["Find Doctor"])
app.include_router(emergency.router, prefix="/emergency", tags=["Emergency"])

@app.get("/")
def root():
    return {
        "message": "HealthAI API is running!",
        "version": "1.0.0"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "api": "HealthAI"}
```

Also update the **Start Command** in Railway Settings to:
```
uvicorn main:app --host 0.0.0.0 --port $PORT --app-dir /app
