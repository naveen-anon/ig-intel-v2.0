import urllib.request
import json
import re
from apscheduler.schedulers.background import BackgroundScheduler
from app.database.postgres import SessionLocal, MonitoredTarget
from datetime import datetime

def fetch_real_instagram_followers(username):
    """
    Direct public JSON token parser with anti-bot headers bypass.
    """
    try:
        # Cleaner approach using a highly responsive alternative viewer API
        url = f"https://api.codetabs.com/v1/proxy/?url=https://www.instagram.com/{username}/?__a=1&__d=dis"
        
        # Sophisticated headers to simulate a real Chrome desktop user agent
        req = urllib.request.Request(
            url, 
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5'
            }
        )
        
        with urllib.request.urlopen(req, timeout=12) as response:
            html_content = response.read().decode('utf-8')

        # Fallback regex if proxy strips structure, checking common public raw variables
        match = re.search(r'"edge_followed_by":\s*\{\s*"count":\s*(\d+)\}', html_content)
        if match:
            return int(match.group(1))
            
        # Second alternative fallback mirror parse strategy
        fallback_url = f"https://imginn.com/p/{username}/"
        fallback_req = urllib.request.Request(fallback_url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'})
        with urllib.request.urlopen(fallback_req, timeout=10) as fb_res:
            fb_html = fb_res.read().decode('utf-8')
            
        fb_match = re.search(r'followers/".*?<span>([\d,k.m]+)</span>', fb_html, re.IGNORECASE | re.DOTALL)
        if fb_match:
            clean_num = fb_match.group(1).replace(',', '').lower()
            if 'k' in clean_num:
                return int(float(clean_num.replace('k', '')) * 1000)
            elif 'm' in clean_num:
                return int(float(clean_num.replace('m', '')) * 1000000)
            return int(clean_num)

    except Exception as e:
        print(f"[⚠️ Live Engine Warning] Network connection blocked or profile private for @{username}")
    return None

def live_monitoring_job():
    db = SessionLocal()
    try:
        active_targets = db.query(MonitoredTarget).filter(MonitoredTarget.is_active == True).all()
        if not active_targets:
            return

        print(f"\n[📡 INSTAGRAM OSINT SYNC - {datetime.now().strftime('%H:%M:%S')}] Querying profiles...")
        
        for target in active_targets:
            live_followers = fetch_real_instagram_followers(target.username)
            
            if live_followers is not None and live_followers > 0:
                target.follower_count_cache = live_followers
                print(f"[🎯 REAL FETCH SUCCESS] @{target.username} -> {live_followers} Followers")
            else:
                # If scraping blocks, it safely retains the dashboard numbers instead of resetting to 0
                print(f"[❌ Scraping Rate-Limited] Retaining last known metric data for @{target.username}")
                
            target.last_checked = datetime.utcnow()
            
        db.commit()
    except Exception as e:
        print(f"[❌ Scheduler Error]: {str(e)}")
        db.rollback()
    finally:
        db.close()

def start_scheduler():
    scheduler = BackgroundScheduler()
    # Dynamic debugging execution loop set to 30 seconds for quick validation on terminal
    scheduler.add_job(live_monitoring_job, 'interval', seconds=30, id='ig_tracker_job', replace_existing=True)
    scheduler.start()
    print("⏱️ OSINT Target Syncer Active. Scanning network pool every 30 seconds.")

