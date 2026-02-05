def get_nutrition_recommendation(calorie_level):
    """
    Rule-based nutrition recommendation
    """

    recommendations = {
        "Low": {
            "Daily_Guidance": "Controlled calorie intake with balanced nutrition.",
            "Foods": {
                "Breakfast": ["Oats", "Boiled egg", "Fruit"],
                "Lunch": ["Brown rice", "Dal", "Vegetables"],
                "Dinner": ["Chapati", "Vegetable curry"],
                "Snacks": ["Fruits", "Nuts (small quantity)"]
            }
        },
        "Medium": {
            "Daily_Guidance": "Balanced diet for healthy growth.",
            "Foods": {
                "Breakfast": ["Idli", "Sambar", "Milk"],
                "Lunch": ["Rice", "Dal", "Curd", "Vegetables"],
                "Dinner": ["Chapati", "Paneer/Egg curry"],
                "Snacks": ["Fruits", "Milk"]
            }
        },
        "High": {
            "Daily_Guidance": "High-energy diet to support growth and activity.",
            "Foods": {
                "Breakfast": ["Oats with milk", "Banana", "Peanut butter"],
                "Lunch": ["Rice", "Dal", "Ghee", "Vegetables"],
                "Dinner": ["Chapati", "Chicken/Paneer"],
                "Snacks": ["Milkshake", "Nuts"]
            }
        }
    }

    return recommendations.get(calorie_level)
