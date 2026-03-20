from datetime import date

from sqlalchemy import Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class VideoMetricDaily(Base):
    __tablename__ = "video_metrics_daily"

    id: Mapped[int] = mapped_column(primary_key=True)
    video_id: Mapped[int] = mapped_column(ForeignKey("videos.id"), index=True)
    date: Mapped[date] = mapped_column(Date)
    views: Mapped[int] = mapped_column(default=0)
    likes: Mapped[int] = mapped_column(default=0)
    comments: Mapped[int] = mapped_column(default=0)
    estimated_watch_time: Mapped[int] = mapped_column(default=0)
    ctr_proxy: Mapped[float] = mapped_column(default=0.0)
    engagement_rate: Mapped[float] = mapped_column(default=0.0)

    video = relationship("Video", back_populates="metrics")


class ChannelMetricDaily(Base):
    __tablename__ = "channel_metrics_daily"

    id: Mapped[int] = mapped_column(primary_key=True)
    channel_id: Mapped[int] = mapped_column(ForeignKey("channels.id"), index=True)
    date: Mapped[date] = mapped_column(Date)
    views: Mapped[int] = mapped_column(default=0)
    watch_time: Mapped[int] = mapped_column(default=0)
    subscribers_gained: Mapped[int] = mapped_column(default=0)
    subscribers_lost: Mapped[int] = mapped_column(default=0)

    channel = relationship("Channel", back_populates="metrics")
