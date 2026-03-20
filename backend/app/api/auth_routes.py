from fastapi import APIRouter, Depends, Query
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.auth import AuthStatusResponse, LoginResponse
from app.services.oauth_service import DEFAULT_SCOPES, OAuthService
from app.services.sync_service import SyncService

router = APIRouter(prefix="/auth", tags=["auth"])
oauth_service = OAuthService()
sync_service = SyncService()


@router.get("/login", response_model=LoginResponse)
def login() -> LoginResponse:
    return LoginResponse(**oauth_service.build_login_payload())


@router.get("/callback")
async def callback(code: str = Query(default="demo-code"), db: Session = Depends(get_db)) -> RedirectResponse:
    await oauth_service.exchange_code(db, code)
    sync_service.ensure_demo_dataset(db)
    return RedirectResponse(url=f"{oauth_service.settings.frontend_url}/overview")


@router.post("/logout")
def logout() -> dict:
    return {"status": "logged_out"}


@router.get("/status", response_model=AuthStatusResponse)
def auth_status() -> AuthStatusResponse:
    issues = [
        "Service accounts are intentionally unsupported for YouTube private user data.",
        "Refresh token rotation should be monitored in production.",
    ]
    return AuthStatusResponse(
        connected=True,
        demo_mode=oauth_service.settings.demo_mode,
        token_expires_at=None,
        scopes=DEFAULT_SCOPES,
        refresh_supported=True,
        issues=issues,
    )
