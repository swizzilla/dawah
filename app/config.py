import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from the directory containing this config file (app directory)
# or from the parent directory (yt-assistant-server)
env_path = Path(__file__).resolve().parent.parent / ".env"
if env_path.exists():
    load_dotenv(env_path)
else:
    # Fallback to default load_dotenv behavior
    load_dotenv()

# Base paths
BASE_DIR = Path(__file__).resolve().parent.parent
CREDENTIALS_DIR = BASE_DIR / "credentials"
TEMP_DIR = BASE_DIR / "temp"

# Ensure directories exist
CREDENTIALS_DIR.mkdir(exist_ok=True)
TEMP_DIR.mkdir(exist_ok=True)

# Domain configuration
DOMAIN_NAME = os.getenv("DOMAIN_NAME", "myserver.c3solutions.co")
SERVER_BASE_URL = f"https://{DOMAIN_NAME}"

# Google OAuth
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET", "")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI", f"{SERVER_BASE_URL}/oauth/callback")
YOUTUBE_SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

# Update the default if GOOGLE_REDIRECT_URI is not set in .env
if os.getenv("GOOGLE_REDIRECT_URI") is None:
    GOOGLE_REDIRECT_URI = f"{SERVER_BASE_URL}/oauth/callback"

# Twilio (for backward compatibility or if still needed)
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER", "")

# Telegram
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "")  # Still needed for backward compatibility
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")
TELEGRAM_API_ID = os.getenv("TELEGRAM_API_ID", "")  # MTProto API ID
TELEGRAM_API_HASH = os.getenv("TELEGRAM_API_HASH", "")  # MTProto API hash
TELEGRAM_PHONE_NUMBER = os.getenv("TELEGRAM_PHONE_NUMBER", "")  # Phone number for MTProto

# Allowed chat IDs (now supports multiple, comma-separated)
ALLOWED_TELEGRAM_CHAT_IDS = os.getenv("ALLOWED_TELEGRAM_CHAT_IDS", "")
if ALLOWED_TELEGRAM_CHAT_IDS:
    ALLOWED_TELEGRAM_CHAT_IDS = [id.strip() for id in ALLOWED_TELEGRAM_CHAT_IDS.split(',')]
else:
    # Fallback to single chat ID for backward compatibility
    single_chat_ids = os.getenv("ALLOWED_TELEGRAM_CHAT_ID", "")
    if single_chat_ids:
        # Split by comma and strip whitespace from each ID
        ALLOWED_TELEGRAM_CHAT_IDS = [id.strip() for id in single_chat_ids.split(',')]
    else:
        ALLOWED_TELEGRAM_CHAT_IDS = []

# Server
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8000))
DEBUG = os.getenv("DEBUG", "false").lower() == "true"

# Database
DATABASE_URL = f"sqlite:///{BASE_DIR}/yt_assistant.db"