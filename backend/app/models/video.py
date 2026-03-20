from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Video(Base):
    __tablename__ = "videos"

    id: Mapped[int] = mapped_column(primary_key=True)
    channel_id: Mapped[int] = mapped_column(ForeignKey("channels.id"), index=True)
    youtube_video_id: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text, default="")
    published_at: Mapped[datetime] = mapped_column(DateTime)
    duration: Mapped[str] = mapped_column(String(32), default="PT0M")
    tags: Mapped[str] = mapped_column(Text, default="")
    category: Mapped[str] = mapped_column(String(120), default="General")

    channel = relationship("Channel", back_populates="videos")
    metrics = relationship("VideoMetricDaily", back_populates="video", cascade="all, delete-orphan")
    recommendations = relationship("Recommendation", back_populates="video", cascade="all, delete-orphan")
