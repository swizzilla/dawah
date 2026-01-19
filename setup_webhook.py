import os
import sys
import httpx
import asyncio
from app.config import TELEGRAM_TOKEN

def register_webhook(webhook_url):
    """Register the webhook with Telegram API"""
    if not TELEGRAM_TOKEN:
        print("❌ Error: TELEGRAM_TOKEN not found in environment!")
        return False
    
    telegram_api_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/setWebhook?url={webhook_url}"
    
    try:
        response = httpx.get(telegram_api_url)
        result = response.json()
        
        if result.get("ok"):
            print(f"✅ Telegram webhook registered successfully: {webhook_url}")
            return True
        else:
            print(f"❌ Failed to register Telegram webhook: {result.get('description')}")
            return False
    except Exception as e:
        print(f"⚠️ Error registering webhook: {str(e)}")
        return False

def main():
    if len(sys.argv) != 2:
        print("Usage: python setup_webhook.py <webhook_url>")
        print("Example: python setup_webhook.py https://your-domain.ngrok-free.dev/telegram/webhook")
        return
    
    webhook_url = sys.argv[1]
    print(f"📡 Registering webhook: {webhook_url}")
    
    success = register_webhook(webhook_url)
    if success:
        print("🎉 Webhook setup completed successfully!")
    else:
        print("💥 Webhook setup failed!")

if __name__ == "__main__":
    main()