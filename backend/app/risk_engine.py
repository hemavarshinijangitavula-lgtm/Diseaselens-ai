"""Transparent demo indicator. Not an official warning or validated hazard model."""
def flood_risk(rain_mm, humidity, wind_kmh, forecast_max_mm=0):
    score = 0
    score += min(max(float(rain_mm or 0), 0) * 0.45, 35)
    score += min(max(float(forecast_max_mm or 0), 0) * 0.35, 35)
    score += min(max(float(humidity or 0), 0) * 0.15, 15)
    score += min(max(float(wind_kmh or 0), 0) * 0.15, 15)
    score = int(round(min(score, 100)))
    level = "Critical" if score >= 75 else "High" if score >= 50 else "Moderate" if score >= 25 else "Low"
    return {"score": score, "level": level, "basis": "prototype weather indicator", "official_warning": False}
