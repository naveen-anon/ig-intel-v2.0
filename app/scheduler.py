import random
from apscheduler.schedulers.background import BackgroundScheduler
from app.database.postgres import SessionLocal, MonitoredTarget
from datetime import datetime

def live_monitoring_job():
    db = SessionLocal()
    try:
        active_targets = db.query(MonitoredTarget).filter(MonitoredTarget.is_active == True).all()
        if not active_targets:
            print("[💤 Scheduler] No active targets to monitor right now.")
            return

        print(f"\n[🔄 Loop Triggered - {datetime.now().strftime('%H:%M:%S')}] Executing target scan...")
        for target in active_targets:
            # --- TESTING ENGINE EXECUTION PLACEHOLDER ---
            # Jab aap scraper jodenge, toh target.follower_count_cache mein live scraper ka data aayega.
            # Abhi execution check karne ke liye hum random number generate kar rahe hain.
            if target.follower_count_cache == 0:
                target.follower_count_cache = random.randint(1000, 5000)
            else:
                target.follower_count_cache += random.randint(-5, 15) # Live increase/decrease simulation
                
            target.last_checked = datetime.utcnow()
            print(f"[🔥 LIVE EXECUTE] Target @{target.username} updated! Followers: {target.follower_count_cache}")
            
        db.commit()
    except Exception as e:
        print(f"[❌ Scheduler Error]: {str(e)}")
        db.rollback()
    finally:
        db.close()

def start_scheduler():
    scheduler = BackgroundScheduler()
    # Testing ke liye isko 10 seconds kar dete hain taaki jaldi-jaldi run ho (Production mein isko badal sakte hain)
    scheduler.add_job(live_monitoring_job, 'interval', seconds=10, id='ig_tracker_job', replace_existing=True)
    scheduler.start()
    print("⏱️ APScheduler Core Engine Active. Running execution cycles every 10 seconds for debugging.")
