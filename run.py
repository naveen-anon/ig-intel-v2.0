import sys
import os
import uvicorn

# System path ko ensure karne ke liye taaki imports fail na ho
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
    
