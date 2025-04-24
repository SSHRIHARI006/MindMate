from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
import numpy as np
import pandas as pd
import joblib
import os
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Load MongoDB URI
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")

# Database client
try:
    client = AsyncIOMotorClient(MONGO_URI)
    db = client.mindmate
    collection = db.predictions
    logger.info("✅ Connected to MongoDB.")
except Exception as e:
    logger.error(f"❌ MongoDB connection failed: {e}")

# Load model and scaler
MODEL_PATH = "/home/shrihari_006/programming/Student_Depression/Models/voting_classifier.pkl"
SCALER_PATH = "/home/shrihari_006/programming/Student_Depression/Models/scaler.pkl"

try:
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    logger.info("✅ Model and Scaler loaded successfully.")
except Exception as e:
    logger.error(f"❌ Error loading model or scaler: {e}")
    model = None
    scaler = None

# Categorical mappings
sleep_map = {"5-6 hours": 0, "7-8 hours": 1, "Less than 5 hours": 2, "More than 8 hours": 3, "Others": 4}
diet_map = {"Healthy": 0, "Moderate": 1, "Others": 2, "Unhealthy": 3}
suicidal_map = {"No": 0, "Yes": 1}

# Likelihood categories
def get_likelihood_level(confidence):
    if confidence <80:
        return "Low"
    elif confidence < 90:
        return "Moderate"
    elif confidence < 95:
        return "High"
    else:
        return "Very High"

# Request body model
class PredictInput(BaseModel):
    sleep: str
    academic: int
    diet: str
    study: float
    stress: int
    suicidal: str

@app.post("/predict")
async def predict(data: PredictInput):
    try:
        logger.info(f"🔍 Received input: {data}")

        if model is None or scaler is None:
            logger.error("Model or Scaler not loaded.")
            raise ValueError("Model or Scaler not loaded.")

        # Map categorical inputs
        sleep = sleep_map.get(data.sleep)
        diet = diet_map.get(data.diet)
        suicidal = suicidal_map.get(data.suicidal)

        if None in (sleep, diet, suicidal):
            logger.error("Invalid categorical input values.")
            raise ValueError("Invalid categorical input values.")

        # Prepare input for model
        input_df = pd.DataFrame([{ 
            "Sleep Duration": sleep,
            "Academic Pressure": data.academic,
            "Dietary Habits": diet,
            "Work/Study Hours": data.study,
            "Financial Stress": data.stress,
            "Have you ever had suicidal thoughts ?": suicidal
        }])

        logger.info(f"📊 Input DataFrame for scaler: {input_df}")

        # Scale and predict
        scaled = scaler.transform(input_df)
        logger.info(f"📏 Scaled input: {scaled}")
        pred = model.predict(scaled)
        proba = model.predict_proba(scaled)

        prediction = int(pred[0])
        confidence = float(np.max(proba)) * 100
        likelihood = get_likelihood_level(confidence)

        logger.info(f"✅ Prediction: {prediction}, Confidence: {confidence:.2f}% -> {likelihood} Likelihood")

        # Save prediction to MongoDB
        record = {
            "input": data.dict(),
            "prediction": "Yes" if prediction == 1 else "No",
            "confidence": confidence,
            "likelihood": likelihood
        }
        await collection.insert_one(record)
      
        suggestions = "Consider using our <a href='/journal'>Journal</a>, browsing <a href='/content'>Resources</a>, or visiting our <a href='/help'>Help</a> section for support and wellness guidance."

        return {
            "likelihood": likelihood,
            "suggestion": suggestions
        }

    except Exception as e:
        logger.error(f"❌ Error during prediction: {e}")
        raise HTTPException(status_code=500, detail=str(e))
