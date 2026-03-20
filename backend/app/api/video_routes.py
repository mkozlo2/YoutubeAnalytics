from statistics import mean

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, selectinload

from app.core.database import get_db
from app.models import Recommendation, Video
from app.schemas.video import RecommendationResponse, VideoDetailResponse, VideoSummaryResponse
from app.services.sync_service import SyncService

router = APIRouter(prefix="/videos", tags=["videos"])
sync_service = SyncService()


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
def list_videos(db: Session = Depends(get_db)) -> list[VideoSummaryResponse]:
    sync_service.ensure_demo_dataset(db)
    videos = db.query(Video).options(selectinload(Video.metrics)).order_by(Video.published_at.desc()).all()
    return [_serialize_video(video) for video in videos]


@router.get("/{video_id}", response_model=VideoDetailResponse)
def get_video(video_id: int, db: Session = Depends(get_db)) -> VideoDetailResponse:
    sync_service.ensure_demo_dataset(db)
    video = (
        db.query(Video)
        .options(selectinload(Video.metrics), selectinload(Video.recommendations))
        .filter(Video.id == video_id)
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
def get_video_recommendations(video_id: int, db: Session = Depends(get_db)) -> list[RecommendationResponse]:
    sync_service.ensure_demo_dataset(db)
    recommendations = db.query(Recommendation).filter(Recommendation.video_id == video_id).all()
    return [RecommendationResponse.model_validate(item) for item in recommendations]
