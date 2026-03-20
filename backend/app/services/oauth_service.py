import secrets
from datetime import datetime, timedelta, timezone
from urllib.parse import urlencode

import httpx
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.security import encrypt_value
from app.models import OAuthToken, User

GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
DEFAULT_SCOPES = [
    "openid",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
    "https://www.googleapis.com/auth/youtube.readonly",
    "https://www.googleapis.com/auth/yt-analytics.readonly",
]


class OAuthService:
    def __init__(self) -> None:
        self.settings = get_settings()

    def is_oauth_configured(self) -> bool:
        return bool(self.settings.google_client_id and self.settings.google_client_secret)

    def build_login_payload(self) -> dict:
        if not self.is_oauth_configured():
            raise HTTPException(
                status_code=400,
                detail="Google OAuth is not configured. Set GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET in your .env file.",
            )
        state = secrets.token_urlsafe(24)
        params = {
            "client_id": self.settings.google_client_id,
            "redirect_uri": self.settings.google_redirect_uri,
            "response_type": "code",
            "scope": " ".join(DEFAULT_SCOPES),
            "access_type": "offline",
            "include_granted_scopes": "true",
            "prompt": "consent",
            "state": state,
        }
        return {
            "authorization_url": f"{GOOGLE_AUTH_URL}?{urlencode(params)}",
            "state": state,
            "demo_mode": self.settings.demo_mode,
            "oauth_configured": True,
        }

    async def exchange_code(self, db: Session, code: str) -> User:
        if not self.is_oauth_configured():
            raise HTTPException(status_code=400, detail="Google OAuth is not configured.")

        async with httpx.AsyncClient(timeout=20) as client:
            response = await client.post(
                GOOGLE_TOKEN_URL,
                data={
                    "code": code,
                    "client_id": self.settings.google_client_id,
                    "client_secret": self.settings.google_client_secret,
                    "redirect_uri": self.settings.google_redirect_uri,
                    "grant_type": "authorization_code",
                },
            )
        if response.is_error:
            raise HTTPException(status_code=400, detail=f"Token exchange failed: {response.text}")

        token_data = response.json()
        user_info = await self.fetch_user_info(token_data["access_token"])
        user = self._ensure_user(
            db,
            email=user_info.get("email", "youtube.partner@example.com"),
            name=user_info.get("name", "Connected Partner"),
        )
        token = OAuthToken(
            user_id=user.id,
            access_token=encrypt_value(token_data["access_token"]),
            refresh_token=encrypt_value(token_data.get("refresh_token", "")),
            expires_at=datetime.now(timezone.utc) + timedelta(seconds=token_data.get("expires_in", 3600)),
        )
        db.add(token)
        db.commit()
        db.refresh(user)
        return user

    async def refresh_access_token(self, refresh_token: str) -> dict:
        if not self.is_oauth_configured():
            raise HTTPException(status_code=400, detail="Google OAuth is not configured.")
        async with httpx.AsyncClient(timeout=20) as client:
            response = await client.post(
                GOOGLE_TOKEN_URL,
                data={
                    "client_id": self.settings.google_client_id,
                    "client_secret": self.settings.google_client_secret,
                    "refresh_token": refresh_token,
                    "grant_type": "refresh_token",
                },
            )
        if response.is_error:
            raise HTTPException(status_code=400, detail=f"Refresh token exchange failed: {response.text}")
        token_data = response.json()
        return {
            "access_token": token_data["access_token"],
            "expires_delta": timedelta(seconds=token_data.get("expires_in", 3600)),
        }

    async def fetch_user_info(self, access_token: str) -> dict:
        async with httpx.AsyncClient(timeout=20) as client:
            response = await client.get(
                "https://www.googleapis.com/oauth2/v2/userinfo",
                headers={"Authorization": f"Bearer {access_token}"},
            )
        if response.is_error:
            raise HTTPException(status_code=400, detail=f"Failed to fetch Google user profile: {response.text}")
        return response.json()

    def _ensure_demo_user(self, db: Session) -> User:
        return self._ensure_user(db, email="demo@partnerplatform.dev", name="Demo Creator")

    def _ensure_user(self, db: Session, email: str, name: str) -> User:
        user = db.query(User).filter(User.email == email).first()
        if user:
            return user
        user = User(email=email, name=name)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
