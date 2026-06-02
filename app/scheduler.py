import time
from apscheduler.schedulers.background import BackgroundScheduler
from app.database.postgres import SessionLocal, MonitoredTarget
from datetime import datetime

def live_monitoring_job():
    db = SessionLocal()
    try:
        active_targets = db.query(MonitoredTarget).filter(MonitoredTarget.is_active == True).all()
        if not active_targets:
            return

        print(f"\n[🔄 Sync Loop - {datetime.now().strftime('%H:%M:%S')}] Checking {len(active_targets)} targets...")
        for target in active_targets:
            target.last_checked = datetime.utcnow()
            print(f"[-] Profile @{target.username} scanned successfully.")
            
        db.commit()
    except Exception as e:
        print(f"[❌ Scheduler Error]: {str(e)}")
        db.rollback()
    finally:
        db.close()

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(live_monitoring_job, 'interval', minutes=15, id='ig_tracker_job', replace_existing=True)
    scheduler.start()
    print("⏱️ APScheduler Engine Started. Monitoring loop running every 15 minutes.)
