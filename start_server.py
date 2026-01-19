import subprocess
import sys
import time
from app.config import TELEGRAM_TOKEN

def start_server():
    """Start the FastAPI server using uvicorn"""
    import uvicorn
    from app.main import app
    
    print("🚀 Starting the FastAPI server with MTProto client...")
    uvicorn.run(app, host="0.0.0.0", port=8000)

def main():
    print("🌟 Starting Dawah application with MTProto client...")
    print("💡 Remember to:")
    print("   1. Update your .env file with your API ID, API hash and phone number")
    print("   2. On first run, you'll need to authenticate with Telegram")
    print("   3. The MTProto client will listen for your messages directly")
    
    # Start server which will initialize MTProto client via lifespan
    start_server()

if __name__ == "__main__":
    main()

if __name__ == "__main__":
    main()