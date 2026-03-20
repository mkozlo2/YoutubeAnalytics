from pydantic import BaseModel

from app.schemas.video import TrendPoint, VideoSummaryResponse


class OverviewResponse(BaseModel):
    total_videos: int
    total_views: int
    total_watch_time_hours: float
    subscriber_count: int
    avg_engagement_rate: float
    upload_frequency_days: float
    top_videos: list[VideoSummaryResponse]
    weakest_videos: list[VideoSummaryResponse]


class TrendsResponse(BaseModel):
    series: list[TrendPoint]
    by_upload_day: list[dict]
    by_category: list[dict]


class QuotaSummaryResponse(BaseModel):
    daily_limit: int
    estimated_used: int
    remaining: int
    expensive_calls: list[dict]
    recommendations: list[str]
