from datetime import datetime, timezone

from fastapi import Cookie, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import decode_session_token, decrypt_value, encrypt_value
from app.models import OAuthToken, User
from app.services.oauth_service import OAuthService


oauth_service = OAuthService()


def get_optional_current_user(
    session_token: str | None = Cookie(default=None),
    db: Session = Depends(get_db),
) -> User | None:
    if not session_token:
        return None
    user_id = decode_session_token(session_token)
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="Signed-in user was not found.")
    return user


def get_current_user(
    user: User | None = Depends(get_optional_current_user),
) -> User:
    if not user:
        raise HTTPException(status_code=401, detail="Sign in with Google or enter demo mode first.")
    return user


async def get_valid_access_token(user: User, db: Session) -> str:
    token = db.query(OAuthToken).filter(OAuthToken.user_id == user.id).order_by(OAuthToken.expires_at.desc()).first()
    if not token:
        raise HTTPException(status_code=401, detail="No OAuth token is stored for this user.")

    if token.expires_at.replace(tzinfo=timezone.utc) > datetime.now(timezone.utc):
        return decrypt_value(token.access_token)

    refreshed = await oauth_service.refresh_access_token(decrypt_value(token.refresh_token))
    token.access_token = encrypt_value(refreshed["access_token"])
    token.expires_at = datetime.now(timezone.utc) + refreshed["expires_delta"]
    db.commit()
    return refreshed["access_token"]
