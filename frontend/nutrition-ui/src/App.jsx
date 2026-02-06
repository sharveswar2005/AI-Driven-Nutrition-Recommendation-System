import { useState } from "react";
import { motion } from "framer-motion";
import "./App.css";

function App() {
  const [formData, setFormData] = useState({
    age: "",
    gender: "Male",
    height_cm: "",
    weight_kg: "",
    activity_level: "Medium",
  });

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResult(null);

    const response = await fetch("http://127.0.0.1:8000/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        age: Number(formData.age),
        gender: formData.gender,
        height_cm: Number(formData.height_cm),
        weight_kg: Number(formData.weight_kg),
        activity_level: formData.activity_level,
      }),
    });

    const data = await response.json();
    setResult(data);
    setLoading(false);
  };

  return (
    <div className="page">
      {/* INPUT CARD */}
      <motion.div
        className="card"
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <h1>AI-Driven Nutrition Recommendation</h1>
        <p className="subtitle">
          Personalized nutrition guidance for children based on health and activity.
        </p>

        <form onSubmit={handleSubmit}>
          <div className="grid">
            <input
              name="age"
              placeholder="Age (years)"
              onChange={handleChange}
              required
            />
            <input
              name="height_cm"
              placeholder="Height (cm)"
              onChange={handleChange}
              required
            />
            <input
              name="weight_kg"
              placeholder="Weight (kg)"
              onChange={handleChange}
              required
            />

            <select name="gender" onChange={handleChange}>
              <option value="Male">Male</option>
              <option value="Female">Female</option>
            </select>

            <select name="activity_level" onChange={handleChange}>
              <option value="Low">Low Activity</option>
              <option value="Medium">Moderate Activity</option>
              <option value="High">High Activity</option>
            </select>
          </div>

          <button type="submit">
            {loading ? "Analyzing..." : "Get Nutrition Plan"}
          </button>
        </form>
      </motion.div>

      {/* RESULT CARD */}
      {result && (
        <motion.div
          className="result-card"
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
        >
          <h2>Health Summary</h2>

          <div className="stats">
            <div className="stat-box">
              <span className="stat-label">BMI</span>
              <span className="stat-value">{result.BMI}</span>
            </div>

            <div className="stat-box">
              <span className="stat-label">Calorie Requirement</span>
              <span className="stat-value">{result.Calorie_Level}</span>
            </div>
          </div>

          <p className="explanation">
            {result.Calorie_Level === "Low" &&
              "Low calorie requirement indicates limited daily energy needs. The focus is on balanced nutrition without excess calories."}

            {result.Calorie_Level === "Medium" &&
              "Medium calorie requirement indicates healthy growth needs with a balanced intake of carbohydrates, proteins, and fats."}

            {result.Calorie_Level === "High" &&
              "High calorie requirement indicates higher energy needs due to growth or activity. A nutrient-dense diet is recommended."}
          </p>

          <h3>Recommended Nutrition Plan</h3>

          {Object.entries(result.Nutrition_Recommendation.Foods).map(
            ([meal, foods]) => (
              <div key={meal} className="meal">
                <strong>{meal}</strong>
                <span>{foods.join(", ")}</span>
              </div>
            )
          )}
        </motion.div>
      )}
    </div>
  );
}

export default App;
