from fastapi import FastAPI, File, UploadFile, HTTPException
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
import numpy as np
from PIL import Image
import io
import os

app = FastAPI()

# Load model
model_path = os.path.join(os.path.dirname(__file__), 'model.h5')
model = load_model(model_path)

# Class mapping
class_mapping = {
    'buahnaga_busuk': 0, 'buahnaga_matang': 1, 'buahnaga_mentah': 2,
    'jeruk_busuk': 3, 'jeruk_matang': 4, 'jeruk_mentah': 5,
    'pepaya mentah': 6, 'pepaya_busuk': 7, 'pepaya_matang': 8,
    'pisang_busuk': 9, 'pisang_matang': 10, 'pisang_mentah': 11,
    'rambutan mentah': 12, 'rambutan_busuk': 13, 'rambutan_matang': 14
}

def preprocess_image(img):
    """Preprocess input image."""
    img = img.resize((224, 224))
    img = img.convert('RGB')
    img_array = img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)  # Normalize for MobileNetV2
    return img_array

def predict_image(img):
    """Predict the class of the image."""
    img_array = preprocess_image(img)
    predictions = model.predict(img_array)
    predicted_class_index = np.argmax(predictions)
    predicted_class = list(class_mapping.keys())[predicted_class_index]
    confidence = predictions[0][predicted_class_index]
    return predicted_class, confidence

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        content = await file.read()
        img = Image.open(io.BytesIO(content))
        predicted_class, confidence = predict_image(img)
        return {
            "predicted_class": predicted_class,
            "confidence": float(confidence)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
