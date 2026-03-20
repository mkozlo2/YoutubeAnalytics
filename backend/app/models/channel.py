from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Channel(Base):
    __tablename__ = "channels"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    youtube_channel_id: Mapped[str] = mapped_column(String(128), unique=True, index=True)
    channel_title: Mapped[str] = mapped_column(String(255))
    subscriber_count: Mapped[int] = mapped_column(default=0)
    video_count: Mapped[int] = mapped_column(default=0)
    view_count: Mapped[int] = mapped_column(default=0)
    last_synced_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    user = relationship("User", back_populates="channels")
    videos = relationship("Video", back_populates="channel", cascade="all, delete-orphan")
    metrics = relationship("ChannelMetricDaily", back_populates="channel", cascade="all, delete-orphan")
