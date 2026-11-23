import requests

BASE = "https://api.open-meteo.com/v1/forecast"
def get_weather(lat: float, lon: float):
    params = {
        "latitude": lat, "longitude": lon,
        "current": "temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m",
        "hourly": "precipitation,temperature_2m,relative_humidity_2m,wind_speed_10m",
        "forecast_days": 3, "timezone": "auto"
    }
    r = requests.get(BASE, params=params, timeout=18)
    r.raise_for_status()
    return r.json()
