from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.core.database import get_db
from app.models import Channel, User
from app.schemas.channel import ChannelResponse
from app.services.sync_service import SyncService

router = APIRouter(prefix="/channels", tags=["channels"])
sync_service = SyncService()


@router.get("/me", response_model=ChannelResponse)
def get_my_channel(user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> ChannelResponse:
    channel = db.query(Channel).filter(Channel.user_id == user.id).first()
    if not channel:
        raise HTTPException(status_code=404, detail="No channel data has been synced yet.")
    return ChannelResponse.model_validate(channel)


@router.post("/sync")
async def sync_channel(user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> dict:
    return await sync_service.sync_channel(db, user)
