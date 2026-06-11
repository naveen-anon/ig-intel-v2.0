import os
import httpx
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse

app = FastAPI(title="Secure Cyber Intel Gateway")

# Environment variables se credentials load karein
CLIENT_ID = os.getenv("META_CLIENT_ID", "YOUR_APP_ID")
CLIENT_SECRET = os.getenv("META_CLIENT_SECRET", "YOUR_APP_SECRET")
REDIRECT_URI = os.getenv("META_REDIRECT_URI", "https://aapka-domain.com/auth/callback")

# Step 1: User ko Authorization ke liye Instagram/Meta Login Page par bhejna
@app.get("/login")
def login_via_instagram():
    # Wo permissions jo aapko account owner se chahiye
    scopes = "instagram_basic,instagram_manage_insights"
    
    # Meta ka official OAuth endpoint
    auth_url = (
        f"https://api.instagram.com/oauth/authorize"
        f"?client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&scope={scopes}"
        f"&response_type=code"
    )
    return RedirectResponse(auth_url)

# Step 2: Token Exchange (Jab user permission de kar wapas aayega)
@app.get("/auth/callback")
async def auth_callback(code: str):
    if not code:
        return {"error": "Authorization failed. No code provided."}
        
    # Is temporary code ko secure Access Token mein convert karna
    token_url = "https://api.instagram.com/oauth/access_token"
    payload = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "authorization_code",
        "redirect_uri": REDIRECT_URI,
        "code": code
    }
    
    async with httpx.AsyncClient() as client:
        # Backend-to-Backend secure request (client browser ko ye nahi dikhega)
        response = await client.post(token_url, data=payload)
        data = response.json()
        
        if "access_token" in data:
            access_token = data["access_token"]
            user_id = data["user_id"]
            
            print(f"[✅ SYSTEM ALERT] New target authenticated. Node ID: {user_id}")
            
            # Step 3: Is token ka use karke account owner ka internal data fetch karna
            internal_data = await fetch_internal_metrics(access_token)
            
            return {
                "status": "Target Synchronized", 
                "node_id": user_id,
                "retrieved_data": internal_data
            }
        else:
            return {"error": "Token exchange failed", "logs": data}

# Step 3: Graph API Engine (Private data nikalne ke liye)
async def fetch_internal_metrics(access_token: str):
    """
    User ke token ka use karke uske internal stats aur private data pull karna.
    """
    # 'me' parameter automatically token wale user ko identify karta hai
    graph_url = f"https://graph.instagram.com/me?fields=id,username,account_type,media_count&access_token={access_token}"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(graph_url)
        return response.json()
      
