import os

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./ig_intel.db")
    
    # Instagram Internal GraphQL Meta (Inspect Element se nikaali hui values)
    # Note: Apne dummy account ki cookies yahan daalein
    INSTA_COOKIE: str = "sessionid=YOUR_DUMMY_SESSION_ID_HERE; csrftoken=XYZ;"
    INSTA_APP_ID: str = "936619743392459" # Standard Instagram Web App ID
    
    # Target profile query hash (Instagram web par user info ke liye fixed hota hai)
    INSTA_QUERY_HASH: str = "69cba7abb54c1cd62241b29c550411d3" 

settings = Settings()
