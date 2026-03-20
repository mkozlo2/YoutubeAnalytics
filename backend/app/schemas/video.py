from datetime import date, datetime

from pydantic import BaseModel


class RecommendationResponse(BaseModel):
    id: int
    type: str
    message: str
    priority: str
    created_at: datetime

    class Config:
        from_attributes = True


class VideoSummaryResponse(BaseModel):
    id: int
    youtube_video_id: str
    title: str
    published_at: datetime
    category: str
    total_views: int
    avg_ctr_proxy: float
    avg_engagement_rate: float
    watch_time_hours: float


class VideoDetailResponse(VideoSummaryResponse):
    description: str
    duration: str
    tags: list[str]
    daily_metrics: list[dict]
    recommendations: list[RecommendationResponse]


class TrendPoint(BaseModel):
    date: date
    views: int
    watch_time: int
    engagement_rate: float
