from datetime import date, datetime

from pydantic import BaseModel


class ChannelResponse(BaseModel):
    id: int
    youtube_channel_id: str
    channel_title: str
    subscriber_count: int
    video_count: int
    view_count: int
    last_synced_at: datetime | None

    class Config:
        from_attributes = True


class DailyChannelMetric(BaseModel):
    date: date
    views: int
    watch_time: int
    subscribers_gained: int
    subscribers_lost: int
