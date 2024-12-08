from fastapi import FastAPI, UploadFile, File, HTTPException
import mysql.connector
import requests
from server.methode import allin

app = FastAPI()

# Database configuration
db_params = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "buah_db"
}
db_connection = mysql.connector.connect(**db_params)
db_cursor = db_connection.cursor()

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        # Kirim file ke service `main.py`
        response = requests.post(
            "http://localhost:8000/predict",
            files={"file": (file.filename, file.file, file.content_type)}
        )
        response.raise_for_status()
        prediction = response.json()
        
        predicted_class = prediction["predicted_class"]
        confidence = prediction["confidence"]
        
        # Simpan hasil ke database
        db_cursor.execute(
            "INSERT INTO predictions (predicted_class, confidence) VALUES (%s, %s)",
            (predicted_class, confidence)
        )
        db_connection.commit()
        
        # Ambil semua data prediksi dari database
        db_cursor.execute("SELECT * FROM predictions")
        results = db_cursor.fetchall()

        # Masukkan data ke objek `allin`
        data_store = allin()
        data_store.add(results)

        return {
            "predicted_class": predicted_class,
            "confidence": float(confidence)
                }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
