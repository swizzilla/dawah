#!/usr/bin/env python3
"""
Start the Dawah application using MTProto client
"""
import subprocess
import sys
import os
from pathlib import Path

def main():
    print("🚀 Starting Dawah application with MTProto client...")
    print("🔧 Checking dependencies...")
    
    # Install dependencies
    print("📦 Installing dependencies...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
    
    print("✅ Dependencies installed")
    
    # Start the application
    print("🎮 Starting MTProto client application...")
    print("💡 Remember to:")
    print("   1. Update your .env file with your API ID, API hash and phone number")
    print("   2. On first run, you'll need to authenticate with Telegram")
    print("   3. The MTProto client will listen for your messages directly")
    
    cmd = [
        "uvicorn", 
        "app.main:app", 
        "--host", "0.0.0.0", 
        "--port", "8000",
        "--reload"
    ]
    
    subprocess.run(cmd)

if __name__ == "__main__":
    main()