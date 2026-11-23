from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import desc
from datetime import datetime
from app.database import SessionLocal, Incident
from app.schemas import IncidentCreate, IncidentStatusUpdate
from app.weather_service import get_weather
from app.risk_engine import flood_risk
from app.ml_model import predict_demo_risk
from app.data_service import SHELTERS, get_demo_alerts
from app.fire_service import get_fire_hotspots, FirmsConfigError, FirmsProviderError


app = FastAPI(title="DisasterLens AI", description="Student disaster monitoring and response prototype", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"], allow_methods=["*"], allow_headers=["*"], allow_credentials=True)

@app.get("/")
def root():
    return {"message": "DisasterLens AI API is running", "prototype": True, "docs": "/docs"}


@app.get("/api/health")
def health():
    return {"status": "ok", "time": datetime.utcnow().isoformat()}


@app.get("/api/weather")
def weather(latitude: float = 13.5503, longitude: float = 78.5029):
    try:
        return get_weather(latitude, longitude)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Weather provider unavailable: {str(e)}")


@app.get("/api/risk")
def risk(latitude: float = 13.5503, longitude: float = 78.5029):
    try:
        data = get_weather(latitude, longitude)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Weather provider unavailable: {str(e)}")
    current = data.get("current", {})
    hourly = data.get("hourly", {})
    precip = current.get("precipitation") or 0
    humidity = current.get("relative_humidity_2m") or 0
    wind = current.get("wind_speed_10m") or 0
    forecast = max(hourly.get("precipitation", [])[:24] or [0])
    result = flood_risk(precip, humidity, wind, forecast)
    ml = predict_demo_risk(precip, forecast, humidity, wind, 100)
    return {"location": {"latitude": latitude, "longitude": longitude}, "weather": current,
            "forecast_max_hourly_rain_mm": forecast, "risk": result, "ml_demo": ml,
            "notice": "Prototype indicator trained/evaluated on synthetic data. Not an official warning or validated hazard forecast."}



@app.get("/api/fire/hotspots")
def fire_hotspots(west: float = 78.0, south: float = 13.0, east: float = 79.0, north: float = 14.0, days: int = 1, source: str = "VIIRS_SNPP_NRT"):
    """Return NASA FIRMS satellite hotspots for a bounding box and recent days."""
    if not (-180 <= west < east <= 180 and -90 <= south < north <= 90):
        raise HTTPException(status_code=400, detail="Invalid bounding box. Require west < east and south < north.")
    if (east - west) > 30 or (north - south) > 30:
        raise HTTPException(status_code=400, detail="Bounding box is too large. Maximum span is 30 degrees per axis.")
    if not 1 <= days <= 5:
        raise HTTPException(status_code=400, detail="days must be between 1 and 5.")
    try:
        rows = get_fire_hotspots(west, south, east, north, days, source)
        return {"source": "NASA FIRMS", "sensor_source": source, "days": days, "bbox": [west, south, east, north], "count": len(rows), "hotspots": rows, "notice": "Satellite thermal detections are hotspots, not confirmed ground fires. Verify with local authorities."}
    except FirmsConfigError as exc:
        raise HTTPException(status_code=503, detail=str(exc))
    except FirmsProviderError as exc:
        raise HTTPException(status_code=502, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

@app.get("/api/incidents")
def list_incidents():
    db: Session = SessionLocal()
    try:
        items = db.query(Incident).order_by(desc(Incident.created_at)).all()
        return [incident_dict(x) for x in items]
    finally:
        db.close()


def incident_dict(x):
    return {"id": x.id, "title": x.title, "disaster_type": x.disaster_type, "severity": x.severity,
            "status": x.status, "description": x.description, "location": x.location,
            "latitude": x.latitude, "longitude": x.longitude, "contact": x.contact,
            "created_at": x.created_at.isoformat() if x.created_at else None}

@app.post("/api/incidents", status_code=201)
def create_incident(payload: IncidentCreate):
    db = SessionLocal()
    try:
        payload_data = payload.model_dump() if hasattr(payload, "model_dump") else payload.dict()
        item = Incident(**payload_data)
        db.add(item); db.commit(); db.refresh(item)
        return incident_dict(item)
    finally:
        db.close()

@app.patch("/api/incidents/{incident_id}/status")
def update_incident_status(incident_id: int, payload: IncidentStatusUpdate):
    allowed = {"Reported", "Monitoring", "Assigned", "Resolved"}
    if payload.status not in allowed:
        raise HTTPException(400, detail=f"Status must be one of {sorted(allowed)}")
    db = SessionLocal()
    try:
        item = db.query(Incident).filter(Incident.id == incident_id).first()
        if not item: raise HTTPException(404, detail="Incident not found")
        item.status = payload.status; db.commit(); db.refresh(item)
        return incident_dict(item)
    finally:
        db.close()

@app.get("/api/shelters")
def shelters():
    return SHELTERS


@app.get("/api/alerts")
def alerts():
    return get_demo_alerts()


@app.get("/api/summary")
def summary():
    db = SessionLocal()
    try:
        incidents = db.query(Incident).all()
        return {"incident_count": len(incidents), "active_incidents": sum(1 for i in incidents if i.status != "Resolved"),
                "resolved_incidents": sum(1 for i in incidents if i.status == "Resolved"),
                "high_severity": sum(1 for i in incidents if i.severity in ("High", "Critical")),
                "shelter_count": len(SHELTERS), "alerts_count": len(get_demo_alerts())}
    finally:
        db.close()
