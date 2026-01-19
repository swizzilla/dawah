from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
import httpx

from app.config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, ALLOWED_TELEGRAM_CHAT_IDS, SERVER_BASE_URL
from app.database import get_db, Account
from app.services.youtube import exchange_code_for_credentials

router = APIRouter()


async def send_telegram_message(chat_id: str, message: str):
    """Send Telegram confirmation - only to the allowed user"""
    if str(chat_id) not in ALLOWED_TELEGRAM_CHAT_IDS:
        # Don't send OAuth confirmations to unauthorized users
        return
    
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    async with httpx.AsyncClient() as client:
        await client.post(url, json={
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "HTML"
        })


@router.get("/callback", response_class=HTMLResponse)
async def oauth_callback(
    request: Request,
    db: Session = Depends(get_db),
    code: str = None,
    state: str = None,
    error: str = None,
):
    """Handle Google OAuth callback"""

    # Simple HTML response
    def html_response(title: str, message: str, success: bool = True):
        color = "#22c55e" if success else "#ef4444"
        return f"""
        <!DOCTYPE html>
        <html>
        <head><title>{title}</title></head>
        <body style="font-family: system-ui; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; background: #111;">
            <div style="text-align: center; color: white;">
                <h1 style="color: {color};">{title}</h1>
                <p>{message}</p>
                <p style="color: #666; margin-top: 2rem;">You can close this window.</p>
            </div>
        </body>
        </html>
        """

    if error:
        return html_response("Authorization Failed", f"Error: {error}", success=False)

    if not code or not state:
        return html_response("Error", "Missing authorization code.", success=False)

    # Parse state: account_id:chat_id
    try:
        parts = state.split(":")
        account_id = int(parts[0])
        chat_id = parts[1] if len(parts) > 1 else None
    except (ValueError, IndexError):
        return html_response("Error", "Invalid state.", success=False)

    # Verify that the chat_id in state is an allowed one
    if chat_id and str(chat_id) not in ALLOWED_TELEGRAM_CHAT_IDS:
        return html_response("Access Denied", "You are not authorized to use this service.", success=False)

    account = db.query(Account).filter(Account.id == account_id).first()
    if not account:
        return html_response("Error", "Account not found.", success=False)

    # Exchange code for credentials
    try:
        exchange_code_for_credentials(code, account.credentials_path)
    except Exception as e:
        return html_response("Authorization Failed", f"Error: {str(e)}", success=False)

    # Send Telegram confirmation
    if chat_id:
        try:
            await send_telegram_message(chat_id, f"Account '{account.name}' authorized! Send 'upload' to start.")
        except Exception:
            pass  # Don't fail if Telegram message fails

    return html_response("Success!", f"Account '{account.name}' is now connected.")