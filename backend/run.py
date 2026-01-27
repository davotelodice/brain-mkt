"""Run FastAPI development server."""
import os
from pathlib import Path

import uvicorn
from dotenv import load_dotenv

# Load .env file from parent directory
env_path = Path(__file__).parent.parent / ".env"
print(f"🔍 Loading .env from: {env_path}")
print(f"✅ File exists: {env_path.exists()}")
load_dotenv(env_path)

# Verify DB URL is loaded
db_url = os.getenv("SUPABASE_DB_URL", "NOT_FOUND")
print(f"🔗 SUPABASE_DB_URL: {db_url[:50]}..." if db_url != "NOT_FOUND" else "❌ SUPABASE_DB_URL not found!")

if __name__ == "__main__":
    port = int(os.getenv("BACKEND_PORT", "8000"))
    host = os.getenv("BACKEND_HOST", "0.0.0.0")
    
    uvicorn.run(
        "src.main:app",
        host=host,
        port=port,
        reload=True,
        log_level="info"
    )
