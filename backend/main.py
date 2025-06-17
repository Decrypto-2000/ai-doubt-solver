from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
import pytesseract
import cv2
import numpy as np
from PIL import Image
import io

# Gemini API key
genai.configure(api_key="AIzaSyAGYCBr7i5cEtPrE196LND2MVgemTMGgOM")  

app = FastAPI()

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Combined endpoint
@app.post("/solve-doubt/")
async def solve_doubt(file: UploadFile = File(...)):
    try:
        # Step 1: OCR
        contents = await file.read()
        image = np.array(Image.open(io.BytesIO(contents)))
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Set path to Tesseract executable (Windows)
        pytesseract.pytesseract.tesseract_cmd = r"C:\Users\Arnab3.Saha\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
        extracted_text = pytesseract.image_to_string(gray).strip()

        if not extracted_text:
            return {"error": "No readable text found in image."}

        # Step 2: Use Gemini to answer
        model = genai.GenerativeModel(model_name="models/gemini-2.0-flash")
        response = model.generate_content(extracted_text)
        answer = response.text.strip()

        return {
            "question": extracted_text,
            "answer": answer
        }

    except Exception as e:
        return {"error": str(e)}
