import os
import pandas as pd
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(
    BASE_DIR, "..", "data", "raw", "children_nutrition_dataset.csv"
)

df = pd.read_csv(DATA_PATH)

print("Dataset loaded successfully")
print("Shape:", df.shape)
print(df.head())

required_columns = [
    "Age",
    "Gender",
    "Height_cm",
    "Weight_kg",
    "BMI",
    "Activity_Level",
    "Daily_Calories",
    "Calorie_Level"
]

missing_cols = set(required_columns) - set(df.columns)
if missing_cols:
    raise ValueError(f"Missing required columns: {missing_cols}")

df = df[(df["Age"] >= 5) & (df["Age"] <= 17)]

final_df = df[
    [
        "Age",
        "Gender",
        "Height_cm",
        "Weight_kg",
        "BMI",
        "Activity_Level",
        "Calorie_Level"
    ]
]

OUTPUT_PATH = os.path.join(
    BASE_DIR, "..", "data", "processed", "children_nutrition_ml_data.csv"
)

os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
final_df.to_csv(OUTPUT_PATH, index=False)

print("Processed dataset saved at:", OUTPUT_PATH)
print("Final shape:", final_df.shape)
