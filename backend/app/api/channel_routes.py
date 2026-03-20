from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models import Channel
from app.schemas.channel import ChannelResponse
from app.services.sync_service import SyncService

router = APIRouter(prefix="/channels", tags=["channels"])
sync_service = SyncService()


@router.get("/me", response_model=ChannelResponse)
def get_my_channel(db: Session = Depends(get_db)) -> ChannelResponse:
    user = sync_service.ensure_demo_dataset(db)
    channel = db.query(Channel).filter(Channel.user_id == user.id).first()
    return ChannelResponse.model_validate(channel)


@router.post("/sync")
def sync_channel(db: Session = Depends(get_db)) -> dict:
    return sync_service.sync_channel(db)
