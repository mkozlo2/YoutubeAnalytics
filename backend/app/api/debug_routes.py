from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.auth import get_optional_current_user
from app.core.database import get_db
from app.models import OAuthToken, SyncLog, User
from app.schemas.analytics import QuotaSummaryResponse
from app.schemas.auth import AuthStatusResponse
from app.services.oauth_service import DEFAULT_SCOPES, OAuthService
from app.services.quota_service import QuotaService

router = APIRouter(prefix="/debug", tags=["debug"])
quota_service = QuotaService()
oauth_service = OAuthService()


@router.get("/sync-logs")
def sync_logs(user: User | None = Depends(get_optional_current_user), db: Session = Depends(get_db)) -> list[dict]:
    if not user:
        return []
    logs = db.query(SyncLog).filter(SyncLog.user_id == user.id).order_by(SyncLog.created_at.desc()).limit(20).all()
    return [
        {
            "id": log.id,
            "status": log.status,
            "endpoint_called": log.endpoint_called,
            "error_message": log.error_message,
            "created_at": log.created_at,
        }
        for log in logs
    ]


@router.get("/quota-summary", response_model=QuotaSummaryResponse)
def quota_summary() -> QuotaSummaryResponse:
    return QuotaSummaryResponse(**quota_service.summary())


@router.get("/auth-status", response_model=AuthStatusResponse)
def auth_status(db: Session = Depends(get_db), user: User | None = Depends(get_optional_current_user)) -> AuthStatusResponse:
    token = None
    if user:
        token = db.query(OAuthToken).filter(OAuthToken.user_id == user.id).order_by(OAuthToken.expires_at.desc()).first()
    issues = [
        "Missing scope simulation should be handled with a reconnect prompt.",
        "Quota exceeded simulation should route users to cached analytics views.",
        "Failed refresh token flows should trigger secure logout and re-authentication.",
    ]
    if not oauth_service.is_oauth_configured():
        issues.insert(0, "Google OAuth credentials are missing, so real sign-in is unavailable until .env is configured.")
    return AuthStatusResponse(
        connected=token is not None,
        demo_mode=oauth_service.settings.demo_mode,
        oauth_configured=oauth_service.is_oauth_configured(),
        token_expires_at=token.expires_at if token else None,
        scopes=DEFAULT_SCOPES,
        refresh_supported=True,
        issues=issues,
    )
