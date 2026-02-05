import os
import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel

from nutrition_rules import get_nutrition_recommendation
print("FastAPI app module loaded successfully")

app = FastAPI(title="AI-Driven Nutrition Recommendation System")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model = joblib.load(os.path.join(BASE_DIR, "model", "calorie_model.pkl"))
feature_encoders = joblib.load(os.path.join(BASE_DIR, "model", "feature_encoders.pkl"))
target_encoder = joblib.load(os.path.join(BASE_DIR, "model", "target_encoder.pkl"))

class ChildInput(BaseModel):
    age: int
    gender: str
    height_cm: float
    weight_kg: float
    activity_level: str

def calculate_bmi(weight, height_cm):
    height_m = height_cm / 100
    return weight / (height_m ** 2)


@app.post("/predict")
def predict_nutrition(data: ChildInput):
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

    return {
        "BMI": round(bmi, 2),
        "Calorie_Level": calorie_level,
        "Nutrition_Recommendation": nutrition_plan
    }
