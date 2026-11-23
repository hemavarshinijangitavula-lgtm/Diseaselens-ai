"""Optional starter ML model trained on synthetic demo data. Clearly not operational forecasting."""
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import numpy as np

FEATURES = ["rainfall_mm", "forecast_rain_mm", "humidity_pct", "wind_kmh", "elevation_m"]

def train_demo_model():
    rng = np.random.default_rng(42)
    n = 1500
    rainfall = rng.uniform(0, 160, n)
    forecast = rng.uniform(0, 200, n)
    humidity = rng.uniform(20, 100, n)
    wind = rng.uniform(0, 100, n)
    elevation = rng.uniform(0, 1200, n)
    # Synthetic label logic for demonstration only; replace with real historical labels.
    score = rainfall * .28 + forecast * .32 + humidity * .12 + wind * .08 - elevation * .025
    y = np.where(score > 80, 2, np.where(score > 42, 1, 0))
    X = np.column_stack([rainfall, forecast, humidity, wind, elevation])
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.2, random_state=42, stratify=y)
    model = RandomForestClassifier(n_estimators=120, random_state=42, class_weight="balanced")
    model.fit(X_train, y_train)
    return model, accuracy_score(y_test, model.predict(X_test))

MODEL, DEMO_ACCURACY = train_demo_model()

def predict_demo_risk(rainfall, forecast_rain, humidity, wind, elevation=100):
    pred = int(MODEL.predict([[rainfall, forecast_rain, humidity, wind, elevation]])[0])
    levels = ["Low", "Moderate", "High"]
    probs = MODEL.predict_proba([[rainfall, forecast_rain, humidity, wind, elevation]])[0]
    return {"level": levels[pred], "probabilities": {levels[i]: round(float(p), 3) for i, p in enumerate(probs)},
            "demo_model": True, "synthetic_training_data": True,
            "accuracy_on_synthetic_test_split": round(float(DEMO_ACCURACY), 3)}
