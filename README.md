# DisasterLens AI — Student Disaster Management Prototype

A full-stack demonstration app for a student disaster-management innovation project. It includes a React dashboard, FastAPI API, SQLite incident registry, weather API integration, interactive OpenStreetMap, shelter demo records, rule-based weather indicator, and a small ML demonstration trained on synthetic data.

> **Safety & data notice:** This is an academic prototype, not a real emergency service. The risk score and synthetic ML model are not validated hazard forecasts. Shelter entries/capacity are illustrative and must be verified. The app does not send official alerts or dispatch rescue teams. Always follow official warnings and emergency services.

## Folder layout

- `backend/app/main.py`: API endpoints
- `backend/app/database.py`: SQLite setup and incident table
- `backend/app/schemas.py`: input validation
- `backend/app/weather_service.py`: Open-Meteo requests
- `backend/app/risk_engine.py`: explainable demo indicator
- `backend/app/ml_model.py`: synthetic-data ML demo
- `backend/app/data_service.py`: prototype alerts/shelters
- `backend/app/seed_data.py`: sample incidents
- `frontend/src/pages`: dashboard pages
- `frontend/src/components`: shared UI components

## Requirements
- Windows 10/11
- Python 3.10+ (3.11/3.12 recommended)
- Node.js LTS and npm
- Internet for Open-Meteo forecast and map tiles

## Backend install and run (PowerShell)
From project root:
```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m app.seed_data
uvicorn app.main:app --reload
```
Open http://127.0.0.1:8000 and API docs at http://127.0.0.1:8000/docs.

If PowerShell blocks virtual environment activation, run this in the same terminal session:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
```

Keep the backend terminal running.

## Frontend install and run
Open a second VS Code terminal at the project root:
```powershell
cd frontend
npm install
npm run dev
```
Open the URL Vite prints (normally http://localhost:5173).

## Prototype pages
- Overview: KPIs, current weather, rainfall graph, risk gauge, map, recent incidents
- Disaster Map: incident/shelter markers and prototype radius overlay
- Weather: current values and forecast graph
- Incidents: report form and status update controls
- Alerts: informational prototype alert feed
- Shelters: sample shelter list and map
- Analytics: charts based on locally stored incident records

## APIs
- `GET /api/health`
- `GET /api/weather?latitude=13.5503&longitude=78.5029`
- `GET /api/risk?latitude=13.5503&longitude=78.5029`
- `GET /api/summary`
- `GET /api/incidents`
- `POST /api/incidents`
- `PATCH /api/incidents/{incident_id}/status`
- `GET /api/shelters`
- `GET /api/alerts`
- `GET /api/fire/hotspots?west=78&south=13&east=79&north=14&days=1&source=VIIRS_SNPP_NRT` (NASA FIRMS, requires MAP_KEY)

## API sample: create incident
POST `/api/incidents` JSON:
```json
{
  "title": "Waterlogging near road",
  "disaster_type": "Flood",
  "severity": "High",
  "description": "Demo report; verify before dispatch.",
  "location": "Example locality",
  "latitude": 13.55,
  "longitude": 78.50,
  "contact": ""
}
```

## Reset demo database
Stop backend and delete `backend/disasterlens.db`, then start again and run:
```powershell
python -m app.seed_data
```

## Suggested next-stage SIH development
1. Replace synthetic ML training labels with a validated, documented historical disaster dataset.
2. Add official warning feeds and source/time metadata; do not scrape or claim official alerts without permission.
3. Add user authentication and role permissions (citizen, responder, admin).
4. Add validated GIS layers (terrain, flood zones, river gauges, road networks) and geospatial calculations.
5. Add safe notification integration (SMS/email) with consent, rate limits, delivery logging and escalation rules.
6. Validate shelter locations, capacity, accessibility and availability with local authorities.
7. Add tests, model evaluation, privacy controls and deployment configuration.

## Advanced Module 1: NASA FIRMS Satellite Fire Hotspots

### What it does
Retrieves recent satellite thermal hotspot detections from NASA FIRMS for a bounding box, displays detections on a Leaflet map, and lists brightness, fire radiative power (FRP), confidence, acquisition date/time and satellite when provided by the source. Hotspots are not confirmed ground fires.

### Setup
1. Request a free NASA FIRMS API MAP_KEY at https://firms.modaps.eosdis.nasa.gov/api/map_key/.
2. Copy `backend/.env.example` to `backend/.env`.
3. Set `NASA_FIRMS_MAP_KEY=your_actual_map_key` in that file. Do not commit/share your key.
4. Install backend dependencies from `backend` with `python -m pip install -r requirements.txt`.
5. Restart FastAPI.
6. In the React dashboard, open **Fire Hotspots** and use bounding box, day count, and satellite source filters.

### API
`GET /api/fire/hotspots?west=78&south=13&east=79&north=14&days=1&source=VIIRS_SNPP_NRT`

Bounding box order: west longitude, south latitude, east longitude, north latitude. This prototype supports 1–5 days (NASA near-real-time area API limit). Sources: VIIRS_SNPP_NRT, VIIRS_NOAA20_NRT, VIIRS_NOAA21_NRT, MODIS_NRT.

### Data disclaimer
Thermal anomalies can include fires, industrial heat, or other hot targets. Do not use as an official warning or as the sole basis for emergency response. Validate detections with local authorities.
