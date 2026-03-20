from statistics import mean

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, selectinload

from app.core.auth import get_current_user
from app.core.database import get_db
from app.models import Channel, Recommendation, User, Video
from app.schemas.video import RecommendationResponse, VideoDetailResponse, VideoSummaryResponse

router = APIRouter(prefix="/videos", tags=["videos"])


def _serialize_video(video: Video) -> VideoSummaryResponse:
    views = sum(metric.views for metric in video.metrics)
    ctrs = [metric.ctr_proxy for metric in video.metrics]
    engagement_rates = [metric.engagement_rate for metric in video.metrics]
    watch_hours = round(sum(metric.estimated_watch_time for metric in video.metrics) / 60, 1)
    return VideoSummaryResponse(
        id=video.id,
        youtube_video_id=video.youtube_video_id,
        title=video.title,
        published_at=video.published_at,
        category=video.category,
        total_views=views,
        avg_ctr_proxy=round(mean(ctrs), 2) if ctrs else 0.0,
        avg_engagement_rate=round(mean(engagement_rates), 2) if engagement_rates else 0.0,
        watch_time_hours=watch_hours,
    )


@router.get("", response_model=list[VideoSummaryResponse])
def list_videos(user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> list[VideoSummaryResponse]:
    videos = (
        db.query(Video)
        .join(Channel, Video.channel_id == Channel.id)
        .options(selectinload(Video.metrics))
        .filter(Channel.user_id == user.id)
        .order_by(Video.published_at.desc())
        .all()
    )
    return [_serialize_video(video) for video in videos]


@router.get("/{video_id}", response_model=VideoDetailResponse)
def get_video(video_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> VideoDetailResponse:
    video = (
        db.query(Video)
        .join(Channel, Video.channel_id == Channel.id)
        .options(selectinload(Video.metrics), selectinload(Video.recommendations))
        .filter(Video.id == video_id, Channel.user_id == user.id)
        .first()
    )
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    summary = _serialize_video(video)
    return VideoDetailResponse(
        **summary.model_dump(),
        description=video.description,
        duration=video.duration,
        tags=[tag.strip() for tag in video.tags.split(",") if tag.strip()],
        daily_metrics=[
            {
                "date": metric.date,
                "views": metric.views,
                "likes": metric.likes,
                "comments": metric.comments,
                "estimated_watch_time": metric.estimated_watch_time,
                "ctr_proxy": metric.ctr_proxy,
                "engagement_rate": metric.engagement_rate,
            }
            for metric in video.metrics
        ],
        recommendations=[RecommendationResponse.model_validate(item) for item in video.recommendations],
    )


@router.get("/{video_id}/recommendations", response_model=list[RecommendationResponse])
def get_video_recommendations(
    video_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[RecommendationResponse]:
    recommendations = (
        db.query(Recommendation)
        .join(Video, Recommendation.video_id == Video.id)
        .join(Channel, Video.channel_id == Channel.id)
        .filter(Recommendation.video_id == video_id, Channel.user_id == user.id)
        .all()
    )
    return [RecommendationResponse.model_validate(item) for item in recommendations]
