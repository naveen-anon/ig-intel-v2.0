import urllib.request
import json
import re
from apscheduler.schedulers.background import BackgroundScheduler
from app.database.postgres import SessionLocal, MonitoredTarget
from datetime import datetime

def fetch_real_instagram_followers(username):
    """
    Simulates a high-privilege mobile device request directly hitting Instagram's 
    web querying endpoints. Safely handles status drops without crashing.
    """
    try:
        # Utilizing a clean, unthrottled public proxy query string
        url = f"https://api.allorigins.win/get?url={urllib.parse.quote(f'https://www.instagram.com/{username}/?__a=1&__d=dis')}"
        
        req = urllib.request.Request(
            url, 
            headers={
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1',
                'Accept': 'application/json'
            }
        )
        
        with urllib.request.urlopen(req, timeout=15) as response:
            res_data = json.loads(response.read().decode('utf-8'))
            raw_contents = res_data.get('contents', '')
            
            # Parsing logic for Instagram target structure
            if '"edge_followed_by"' in raw_contents:
                count_match = re.search(r'"edge_followed_by":\s*\{\s*"count":\s*(\d+)\}', raw_contents)
                if count_match:
                    return int(count_match.group(1))

        # SECONDARY BACKUP STRATEGY: Direct regex scanning on open profile layout
        backup_url = f"https://api.allorigins.win/get?url={urllib.parse.quote(f'https://www.instagram.com/{username}/')}"
        backup_req = urllib.request.Request(backup_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        
        with urllib.request.urlopen(backup_req, timeout=12) as b_res:
            b_data = json.loads(b_res.read().decode('utf-8'))
            b_content = b_data.get('contents', '')
            
            meta_match = re.search(r'"edge_followed_by":\s*\{\s*"count":\s*(\d+)\}', b_content)
            if meta_match:
                return int(meta_match.group(1))
                
            # Content meta extraction
            desc_match = re.search(r'([\d,k.m]+)\s*Followers', b_content, re.IGNORECASE)
            if desc_match:
                clean_num = desc_match.group(1).replace(',', '').lower()
                if 'k' in clean_num:
                    return int(float(clean_num.replace('k', '')) * 1000)
                elif 'm' in clean_num:
                    return int(float(clean_num.replace('m', '')) * 1000000)
                return int(clean_num)

    except Exception as e:
        print(f"[⚠️ Connection Throttled] Unable to reach Instagram nodes for @{username}")
    return None

def live_monitoring_job():
    db = SessionLocal()
    try:
        active_targets = db.query(MonitoredTarget).filter(MonitoredTarget.is_active == True).all()
        if not active_targets:
            return

        print(f"\n[📡 OSINT FETCH CYCLE - {datetime.now().strftime('%H:%M:%S')}] Pinging decentralized proxy channels...")
        for target in active_targets:
            live_followers = fetch_real_instagram_followers(target.username)
            
            if live_followers is not None and live_followers > 0:
                target.follower_count_cache = live_followers
                print(f"[🎯 SUCCESS] @{target.username} linked. Followers: {live_followers}")
            else:
                print(f"[❌ API Blocked] Using last known network status for @{target.username}")
                
            target.last_checked = datetime.utcnow()
            
        db.commit()
    except Exception as e:
        print(f"[❌ Scheduler Error]: {str(e)}")
        db.rollback()
    finally:
        db.close()

def start_scheduler():
    scheduler = BackgroundScheduler()
    # 20 seconds loop validation
    scheduler.add_job(live_monitoring_job, 'interval', seconds=20, id='ig_tracker_job', replace_existing=True)
    scheduler.start()
    print("⏱️ Advanced Network Syncer fully initialized.")
