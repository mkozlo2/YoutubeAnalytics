from fastapi import APIRouter, Depends, HTTPException, Query, Response
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.core.auth import get_optional_current_user
from app.core.database import get_db
from app.core.security import create_session_token
from app.models import OAuthToken
from app.schemas.auth import AuthStatusResponse, LoginResponse
from app.services.oauth_service import DEFAULT_SCOPES, OAuthService
from app.services.sync_service import SyncService

router = APIRouter(prefix="/auth", tags=["auth"])
oauth_service = OAuthService()
sync_service = SyncService()


@router.get("/login", response_model=LoginResponse)
def login() -> LoginResponse:
    return LoginResponse(**oauth_service.build_login_payload())


@router.get("/login/redirect")
def login_redirect() -> RedirectResponse:
    payload = oauth_service.build_login_payload()
    return RedirectResponse(url=payload["authorization_url"])


@router.get("/demo")
def demo_login(db: Session = Depends(get_db)) -> RedirectResponse:
    user = sync_service.ensure_demo_dataset(db)
    response = RedirectResponse(url=f"{oauth_service.settings.frontend_url}/overview")
    response.set_cookie("session_token", create_session_token(user.id), httponly=True, samesite="lax")
    return response


@router.get("/callback")
async def callback(code: str | None = Query(default=None), db: Session = Depends(get_db)) -> RedirectResponse:
    if not code:
        raise HTTPException(status_code=400, detail="Missing OAuth authorization code.")
    user = await oauth_service.exchange_code(db, code)
    try:
        await sync_service.sync_channel(db, user)
    except HTTPException:
        pass
    response = RedirectResponse(url=f"{oauth_service.settings.frontend_url}/overview")
    response.set_cookie("session_token", create_session_token(user.id), httponly=True, samesite="lax")
    return response


@router.post("/logout")
def logout(response: Response) -> dict:
    response.delete_cookie("session_token")
    return {"status": "logged_out"}


@router.get("/status", response_model=AuthStatusResponse)
def auth_status(
    db: Session = Depends(get_db),
    user=Depends(get_optional_current_user),
) -> AuthStatusResponse:
    token = None
    if user:
        token = db.query(OAuthToken).filter(OAuthToken.user_id == user.id).order_by(OAuthToken.expires_at.desc()).first()
    issues = [
        "Service accounts are intentionally unsupported for YouTube private user data.",
        "Refresh token rotation should be monitored in production.",
    ]
    if not oauth_service.is_oauth_configured():
        issues.insert(0, "Google OAuth credentials are not configured in the backend environment.")
    return AuthStatusResponse(
        connected=token is not None,
        demo_mode=oauth_service.settings.demo_mode,
        oauth_configured=oauth_service.is_oauth_configured(),
        token_expires_at=token.expires_at if token else None,
        scopes=DEFAULT_SCOPES,
        refresh_supported=True,
        issues=issues,
    )
