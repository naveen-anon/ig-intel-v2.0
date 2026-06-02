import os
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database.postgres import init_pg_db, SessionLocal, MonitoredTarget
from app.scheduler import start_scheduler
from datetime import datetime

app = FastAPI(title="IG-Intel Live Monitoring OSINT API", version="2.0")

# Setup HTML frontend engine
templates = Jinja2Templates(directory="templates")

# STARTUP ACTION: Initialize database and monitoring schedule loops
@app.on_event("startup")
def startup_event():
    init_pg_db()       
    start_scheduler()  
    print("🚀 IG-Intel V2 System Engine Online & Monitoring Live...")

# Dependency to manage database transactions
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# FRONTEND UI ROUTE: Serves the web dashboard
@app.get("/", response_class=HTMLResponse)
async def read_dashboard(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# API ROUTE: Returns list of monitored targets to UI
@app.get("/monitor/list")
def list_monitored_targets(db: Session = Depends(get_db)):
    return db.query(MonitoredTarget).all()

# API ROUTE: Add profile to tracker
@app.post("/monitor/add/{username}")
def add_target_to_monitor(username: str, db: Session = Depends(get_db)):
    existing = db.query(MonitoredTarget).filter(MonitoredTarget.username == username).first()
    if existing:
        if existing.is_active:
            return {"message": f"@{username} is already being monitored live."}
        existing.is_active = True
        db.commit()
        return {"message": f"Live monitoring re-activated for @{username}."}
        
    new_target = MonitoredTarget(username=username, is_active=True, last_checked=datetime.utcnow())
    db.add(new_target)
    db.commit()
    return {"status": "success", "message": f"@{username} added to 24/7 Live Monitoring Queue."}

# API ROUTE: Stop tracking profile
@app.post("/monitor/stop/{username}")
def stop_monitoring(username: str, db: Session = Depends(get_db)):
    target = db.query(MonitoredTarget).filter(MonitoredTarget.username == username).first()
    if not target:
        raise HTTPException(status_code=404, detail="Target not found in monitoring list.")
    target.is_active = False
    db.commit()
    return {"message": f"Live monitoring stopped for @{username}."}
  
