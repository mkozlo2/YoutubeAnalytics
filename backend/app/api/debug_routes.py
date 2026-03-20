from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models import SyncLog
from app.schemas.analytics import QuotaSummaryResponse
from app.schemas.auth import AuthStatusResponse
from app.services.oauth_service import DEFAULT_SCOPES, OAuthService
from app.services.quota_service import QuotaService
from app.services.sync_service import SyncService

router = APIRouter(prefix="/debug", tags=["debug"])
quota_service = QuotaService()
oauth_service = OAuthService()
sync_service = SyncService()


@router.get("/sync-logs")
def sync_logs(db: Session = Depends(get_db)) -> list[dict]:
    sync_service.ensure_demo_dataset(db)
    logs = db.query(SyncLog).order_by(SyncLog.created_at.desc()).limit(20).all()
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
def auth_status() -> AuthStatusResponse:
    issues = [
        "Missing scope simulation should be handled with a reconnect prompt.",
        "Quota exceeded simulation should route users to cached analytics views.",
        "Failed refresh token flows should trigger secure logout and re-authentication.",
    ]
    return AuthStatusResponse(
        connected=True,
        demo_mode=oauth_service.settings.demo_mode,
        token_expires_at=None,
        scopes=DEFAULT_SCOPES,
        refresh_supported=True,
        issues=issues,
    )
