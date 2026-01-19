import httpx
from app.config import TELEGRAM_TOKEN

def register_webhook():
    """Register the webhook with Telegram API for the specific domain"""
    if not TELEGRAM_TOKEN:
        print("❌ Error: TELEGRAM_TOKEN not found in environment!")
        return False
    
    # Using the specific domain
    webhook_url = "https://myserver.c3solutions.co/telegram/webhook"
    telegram_api_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/setWebhook?url={webhook_url}"
    
    try:
        response = httpx.get(telegram_api_url)
        result = response.json()
        
        if result.get("ok"):
            print(f"✅ Telegram webhook registered successfully for domain: {webhook_url}")
            print("🤖 Your bot is now ready to receive messages!")
            return True
        else:
            print(f"❌ Failed to register Telegram webhook: {result.get('description')}")
            return False
    except Exception as e:
        print(f"⚠️ Error registering webhook: {str(e)}")
        return False

if __name__ == "__main__":
    print("📡 Registering webhook for myserver.c3solutions.co...")
    print("⚠️  WARNING: Traditional webhook registration is deprecated!")
    print("🔄 This application now uses MTProto client for direct message handling.")
    print("💡 Use start_mtproto.py to run the application with MTProto client instead.")
    print("🔐 The MTProto approach offers direct access to your account and better functionality.")
    success = register_webhook()
    if success:
        print("🎉 Webhook registration completed successfully!")
    else:
        print("💥 Webhook registration failed!")
        print("💡 Make sure your server is running and accessible at https://myserver.c3solutions.co")