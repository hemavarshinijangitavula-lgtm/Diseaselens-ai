from datetime import datetime, timezone
# Seeded demo shelters/locations. Verify locations and capacity before real-world use.
SHELTERS = [
    {"id": "S-01", "name": "Community Relief Center", "location": "Madanapalle", "latitude": 13.5503, "longitude": 78.5029, "capacity": 250, "available": 120, "services": ["Food", "Water", "First aid"]},
    {"id": "S-02", "name": "District School Shelter", "location": "Chittoor", "latitude": 13.2172, "longitude": 79.1003, "capacity": 400, "available": 210, "services": ["Food", "Family support"]},
    {"id": "S-03", "name": "Temporary Relief Camp", "location": "Tirupati", "latitude": 13.6288, "longitude": 79.4192, "capacity": 300, "available": 95, "services": ["Water", "Medical"]},
]

def get_demo_alerts():
    now = datetime.now(timezone.utc).isoformat()
    return [
        {"id": "A-001", "title": "Weather monitoring active", "severity": "Info", "location": "Madanapalle region", "message": "Weather indicators are being monitored. Check official bulletins for warnings.", "time": now},
        {"id": "A-002", "title": "Prototype notice", "severity": "Info", "location": "System", "message": "This dashboard is a student prototype. Alerts are not official or automatically dispatched.", "time": now},
    ]
