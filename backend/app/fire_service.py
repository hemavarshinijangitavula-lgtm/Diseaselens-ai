"""NASA FIRMS satellite hotspot retrieval service. Requires a free FIRMS MAP_KEY."""
import csv
import io
import os
import requests
from dotenv import load_dotenv

load_dotenv()
FIRMS_API_BASE = "https://firms.modaps.eosdis.nasa.gov/api/area/csv"
ALLOWED_SOURCES = {"VIIRS_SNPP_NRT", "VIIRS_NOAA20_NRT", "VIIRS_NOAA21_NRT", "MODIS_NRT"}

class FirmsConfigError(RuntimeError):
    pass

class FirmsProviderError(RuntimeError):
    pass

def parse_hotspot_csv(csv_text: str):
    """Parse FIRMS CSV and normalize fields for the frontend."""
    rows = []
    reader = csv.DictReader(io.StringIO(csv_text))
    for row in reader:
        try:
            lat = float(row.get("latitude", ""))
            lon = float(row.get("longitude", ""))
        except (TypeError, ValueError):
            continue
        def number(name):
            try: return float(row.get(name, ""))
            except (TypeError, ValueError): return None
        rows.append({
            "latitude": lat,
            "longitude": lon,
            "brightness": number("bright_ti4") if number("bright_ti4") is not None else number("brightness"),
            "frp": number("frp"),
            "confidence": row.get("confidence"),
            "satellite": row.get("satellite"),
            "instrument": row.get("instrument"),
            "acquisition_date": row.get("acq_date"),
            "acquisition_time": row.get("acq_time"),
            "daynight": row.get("daynight"),
        })
    return rows

def get_fire_hotspots(west: float, south: float, east: float, north: float, days: int = 1, source: str = "VIIRS_SNPP_NRT"):
    key = os.getenv("NASA_FIRMS_MAP_KEY", "").strip()
    if not key or key.lower() in {"your_map_key_here", "changeme"}:
        raise FirmsConfigError("NASA FIRMS MAP_KEY is missing. Add NASA_FIRMS_MAP_KEY to backend/.env.")
    if source not in ALLOWED_SOURCES:
        raise ValueError(f"Unsupported FIRMS source. Allowed sources: {', '.join(sorted(ALLOWED_SOURCES))}")
    if not 1 <= days <= 5:
        raise ValueError("days must be between 1 and 5 for this near-real-time endpoint")
    area = f"{west},{south},{east},{north}"
    url = f"{FIRMS_API_BASE}/{key}/{source}/{area}/{days}"
    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 401 or response.status_code == 403:
            raise FirmsProviderError("NASA FIRMS rejected the MAP_KEY. Verify your key in backend/.env.")
        response.raise_for_status()
    except requests.RequestException as exc:
        raise FirmsProviderError(f"NASA FIRMS request failed: {exc}") from exc
    text = response.text.strip()
    if not text:
        return []
    if text.lower().startswith("error") or "invalid map key" in text.lower():
        raise FirmsProviderError("NASA FIRMS returned an error. Check your MAP_KEY and selected source.")
    return parse_hotspot_csv(text)
