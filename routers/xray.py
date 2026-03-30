from fastapi import APIRouter, UploadFile, File
import numpy as np
from PIL import Image
import onnxruntime as ort
import io
import os

router = APIRouter()

model_path = os.path.join(os.path.dirname(__file__), '..', 'models', 'xray_model.onnx')

try:
    session = ort.InferenceSession(model_path)
    print("✅ X-Ray model loaded!")
except Exception as e:
    print(f"❌ X-Ray model error: {e}")
    session = None

@router.post("/xray")
async def analyze_xray(file: UploadFile = File(...)):
    try:
        if session is None:
            return {"error": "Model not loaded"}

        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert('RGB')
        image = image.resize((150, 150))
        img_array = np.array(image, dtype=np.float32) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        input_name = session.get_inputs()[0].name
        prediction = session.run(None, {input_name: img_array})[0]
        probability = float(prediction[0][0])

        return {
            "prediction": "Pneumonia" if probability > 0.5 else "Normal",
            "probability": probability,
            "confidence": f"{probability*100:.1f}%" if probability > 0.5 else f"{(1-probability)*100:.1f}%",
            "is_pneumonia": probability > 0.5
        }
    except Exception as e:
        return {"error": str(e)}
