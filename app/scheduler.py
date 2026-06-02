import urllib.request
import json
import re
from apscheduler.schedulers.background import BackgroundScheduler
from app.database.postgres import SessionLocal, MonitoredTarget
from datetime import datetime

def fetch_real_instagram_followers(username):
    """Bina login ke public mirror se live follower count nikalne ka tareeka"""
    try:
        # Instagram public viewer mirror URL
        url = f"https://imginn.com/p/{username}/"
        
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        )
        
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode('utf-8')
            
        # HTML ke andar se followers count nikalne ke liye Regex Matching
        # Note: Agar third-party website ka UI badalta hai, toh regex update karna pad sakta hai
        match = re.search(r'href="/p/[^"]+/followers/">\s*<span>([\d,k.m]+)</span>', html, re.IGNORECASE)
        
        if match:
            clean_num = match.group(1).replace(',', '').lower()
            if 'k' in clean_num:
                return int(float(clean_num.replace('k', '')) * 1000)
            elif 'm' in clean_num:
                return int(float(clean_num.replace('m', '')) * 1000000)
            return int(clean_num)
            
    except Exception as e:
        print(f"[⚠️ Scraper Warning] Could not fetch live data for @{username}: {str(e)}")
    return None

def live_monitoring_job():
    db = SessionLocal()
    try:
        active_targets = db.query(MonitoredTarget).filter(MonitoredTarget.is_active == True).all()
        if not active_targets:
            return

        print(f"\n[📡 LIVE OSINT SCAN - {datetime.now().strftime('%H:%M:%S')}] Connecting to Instagram Network...")
        
        for target in active_targets:
            # SIMULATOR KHATAM -> REAL SCRAPER START
            live_followers = fetch_real_instagram_followers(target.username)
            
            if live_followers is not None:
                target.follower_count_cache = live_followers
                print(f"[🎯 REAL FETCH SUCCESS] @{target.username} -> {live_followers} Followers")
            else:
                print(f"[❌ Fetch Failed] Using last cached value for @{target.username}")
                
            target.last_checked = datetime.utcnow()
            
        db.commit()
    except Exception as e:
        print(f"[❌ Scheduler Error]: {str(e)}")
        db.rollback()
    finally:
        db.close()

def start_scheduler():
    scheduler = BackgroundScheduler()
    # Real scraping mein baar-baar jaldi request bhejne se IP block ho sakti hai
    # Isliye real data ke liye interval ko 5 se 15 minute rakhna sahi hota hai
    scheduler.add_job(live_monitoring_job, 'interval', minutes=10, id='ig_tracker_job', replace_existing=True)
    scheduler.start()
    print("⏱️ APScheduler Core Engine Active. Real OSINT scanning loops set to 10 minutes.")
