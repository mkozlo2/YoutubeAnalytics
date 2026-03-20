from statistics import mean

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, selectinload

from app.core.auth import get_current_user
from app.core.database import get_db
from app.models import Channel, User, Video
from app.schemas.analytics import OverviewResponse, TrendsResponse
from app.schemas.video import TrendPoint, VideoSummaryResponse

router = APIRouter(prefix="/analytics", tags=["analytics"])


def _video_rows(videos: list[Video]) -> list[dict]:
    rows = []
    for video in videos:
        views = sum(metric.views for metric in video.metrics)
        rows.append(
            {
                "id": video.id,
                "youtube_video_id": video.youtube_video_id,
                "title": video.title,
                "published_at": video.published_at,
                "category": video.category,
                "total_views": views,
                "avg_ctr_proxy": round(mean([metric.ctr_proxy for metric in video.metrics]), 2),
                "avg_engagement_rate": round(mean([metric.engagement_rate for metric in video.metrics]), 2),
                "watch_time_hours": round(sum(metric.estimated_watch_time for metric in video.metrics) / 60, 1),
            }
        )
    return rows


@router.get("/overview", response_model=OverviewResponse)
def overview(user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> OverviewResponse:
    channel = (
        db.query(Channel)
        .options(selectinload(Channel.videos).selectinload(Video.metrics))
        .filter(Channel.user_id == user.id)
        .first()
    )
    videos = channel.videos if channel else []
    rows = sorted(_video_rows(videos), key=lambda item: item["total_views"], reverse=True)
    row_models = [VideoSummaryResponse(**row) for row in rows]
    engagement_samples = [row["avg_engagement_rate"] for row in rows] or [0]
    upload_frequency_days = 0.0
    if len(videos) > 1:
        ordered = sorted((video.published_at for video in videos), reverse=True)
        gaps = [(ordered[index] - ordered[index + 1]).days for index in range(len(ordered) - 1)]
        upload_frequency_days = round(mean(gaps), 1)
    return OverviewResponse(
        total_videos=len(videos),
        total_views=sum(row["total_views"] for row in rows),
        total_watch_time_hours=round(sum(row["watch_time_hours"] for row in rows), 1),
        subscriber_count=channel.subscriber_count if channel else 0,
        avg_engagement_rate=round(mean(engagement_samples), 2),
        upload_frequency_days=upload_frequency_days,
        top_videos=row_models[:3],
        weakest_videos=list(reversed(row_models[-3:])),
    )


@router.get("/trends", response_model=TrendsResponse)
def trends(user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> TrendsResponse:
    channel = db.query(Channel).options(selectinload(Channel.metrics), selectinload(Channel.videos)).filter(Channel.user_id == user.id).first()
    series = [
        TrendPoint(
            date=metric.date,
            views=metric.views,
            watch_time=metric.watch_time,
            engagement_rate=round((metric.subscribers_gained / max(metric.views, 1)) * 100, 2),
        )
        for metric in (channel.metrics if channel else [])
    ]
    by_upload_day: dict[str, int] = {}
    by_category: dict[str, int] = {}
    for video in channel.videos if channel else []:
        day = video.published_at.strftime("%A")
        by_upload_day[day] = by_upload_day.get(day, 0) + 1
        by_category[video.category] = by_category.get(video.category, 0) + 1
    return TrendsResponse(
        series=series,
        by_upload_day=[{"day": key, "videos": value} for key, value in by_upload_day.items()],
        by_category=[{"category": key, "videos": value} for key, value in by_category.items()],
    )


@router.get("/top-videos")
def top_videos(user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> list[dict]:
    videos = (
        db.query(Video)
        .join(Channel, Video.channel_id == Channel.id)
        .options(selectinload(Video.metrics))
        .filter(Channel.user_id == user.id)
        .all()
    )
    return sorted(_video_rows(videos), key=lambda item: item["total_views"], reverse=True)[:5]


@router.get("/underperforming-videos")
def underperforming_videos(user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> list[dict]:
    videos = (
        db.query(Video)
        .join(Channel, Video.channel_id == Channel.id)
        .options(selectinload(Video.metrics))
        .filter(Channel.user_id == user.id)
        .all()
    )
    return sorted(_video_rows(videos), key=lambda item: item["avg_ctr_proxy"])[:5]
