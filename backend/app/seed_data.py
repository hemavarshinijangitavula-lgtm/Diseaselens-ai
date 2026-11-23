from app.database import SessionLocal, Incident

def seed():
    db = SessionLocal()
    try:
        if db.query(Incident).count() == 0:
            records = [
                Incident(title="Heavy rainfall watch", disaster_type="Flood", severity="Moderate", status="Monitoring", description="Demo record for dashboard presentation.", location="Madanapalle", latitude=13.5503, longitude=78.5029),
                Incident(title="Road access assessment", disaster_type="Landslide", severity="Low", status="Reported", description="Demo record. Field verification required.", location="Chittoor district", latitude=13.2172, longitude=79.1003),
                Incident(title="Heat monitoring", disaster_type="Heatwave", severity="High", status="Monitoring", description="Demo record. Consult official weather advisories.", location="Tirupati", latitude=13.6288, longitude=79.4192),
            ]
            db.add_all(records)
            db.commit()
    finally:
        db.close()
if __name__ == "__main__":
    seed()
