import os
import joblib
import pandas as pd
from datetime import datetime

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session

from nutrition_rules import get_nutrition_recommendation
from database import SessionLocal
from models import Prediction, User
from auth import get_current_user
from routes_auth import router as auth_router


# ---------------- APP CONFIG ---------------- #

app = FastAPI(
    title="AI-Driven Nutrition Recommendation System",
    description="Predicts calorie level and recommends nutrition for children",
    version="2.0"
)

print("FastAPI app module loaded successfully")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)


# ---------------- LOAD ML MODELS ---------------- #

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model = joblib.load(os.path.join(BASE_DIR, "model", "calorie_model.pkl"))
feature_encoders = joblib.load(os.path.join(BASE_DIR, "model", "feature_encoders.pkl"))
target_encoder = joblib.load(os.path.join(BASE_DIR, "model", "target_encoder.pkl"))


# ---------------- DB DEPENDENCY ---------------- #

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------- SCHEMAS ---------------- #

class ChildInput(BaseModel):
    age: int
    gender: str
    height_cm: float
    weight_kg: float
    activity_level: str


# ---------------- HELPERS ---------------- #

def calculate_bmi(weight_kg: float, height_cm: float) -> float:
    height_m = height_cm / 100
    return weight_kg / (height_m ** 2)


# ---------------- ROUTES ---------------- #

@app.get("/")
def health_check():
    return {"status": "API is running"}


@app.post("/predict")
def predict_nutrition(
    data: ChildInput,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Protected route:
    - Predicts calorie level
    - Stores prediction in DB
    - Returns nutrition plan
    """

    bmi = calculate_bmi(data.weight_kg, data.height_cm)

    input_df = pd.DataFrame([{
        "Age": data.age,
        "Gender": data.gender,
        "Height_cm": data.height_cm,
        "Weight_kg": data.weight_kg,
        "BMI": bmi,
        "Activity_Level": data.activity_level
    }])

    for col, encoder in feature_encoders.items():
        input_df[col] = encoder.transform(input_df[col])

    prediction = model.predict(input_df)[0]
    calorie_level = target_encoder.inverse_transform([prediction])[0]

    nutrition_plan = get_nutrition_recommendation(calorie_level)

    # ---------------- SAVE TO DB ---------------- #

    record = Prediction(
        user_id=current_user.id,
        age=data.age,
        gender=data.gender,
        height_cm=data.height_cm,
        weight_kg=data.weight_kg,
        activity_level=data.activity_level,
        bmi=round(bmi, 2),
        calorie_level=calorie_level,
        created_at=datetime.utcnow()
    )

    db.add(record)
    db.commit()

    return {
        "BMI": round(bmi, 2),
        "Calorie_Level": calorie_level,
        "Nutrition_Recommendation": nutrition_plan
    }


@app.get("/history")
def get_prediction_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Returns all past predictions of logged-in user
    """

    records = (
        db.query(Prediction)
        .filter(Prediction.user_id == current_user.id)
        .order_by(Prediction.created_at.desc())
        .all()
    )

    return [
        {
            "bmi": r.bmi,
            "calorie_level": r.calorie_level,
            "date": r.created_at
        }
        for r in records
    ]
