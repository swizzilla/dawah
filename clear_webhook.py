import httpx
from app.config import TELEGRAM_TOKEN

def clear_webhook():
    """Clear the currently registered webhook"""
    if not TELEGRAM_TOKEN:
        print("❌ Error: TELEGRAM_TOKEN not found in environment!")
        return False
    
    # Setting an empty URL clears the webhook
    telegram_api_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/setWebhook"
    
    try:
        response = httpx.get(telegram_api_url)
        result = response.json()
        
        if result.get("ok"):
            print(f"✅ Telegram webhook cleared successfully")
            print("🤖 Webhook has been removed. MTProto client will handle messages directly.")
            return True
        else:
            print(f"❌ Failed to clear Telegram webhook: {result.get('description')}")
            return False
    except Exception as e:
        print(f"⚠️ Error clearing webhook: {str(e)}")
        return False

if __name__ == "__main__":
    print("📡 Clearing registered webhook...")
    success = clear_webhook()
    if success:
        print("🎉 Webhook clearing completed successfully!")
    else:
        print("💥 Webhook clearing failed!")