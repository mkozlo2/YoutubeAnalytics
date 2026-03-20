from datetime import datetime
from statistics import mean

from sqlalchemy.orm import Session, selectinload

from app.models import Channel, ChannelMetricDaily, Recommendation, SyncLog, User, Video, VideoMetricDaily
from app.services.recommendation_service import RecommendationService
from app.services.youtube_analytics_service import YouTubeAnalyticsService
from app.services.youtube_data_service import YouTubeDataService


class SyncService:
    def __init__(self) -> None:
        self.data_service = YouTubeDataService()
        self.analytics_service = YouTubeAnalyticsService()
        self.recommendation_service = RecommendationService()

    def ensure_demo_dataset(self, db: Session) -> User:
        user = db.query(User).filter(User.email == "demo@partnerplatform.dev").first()
        if not user:
            user = User(email="demo@partnerplatform.dev", name="Demo Creator")
            db.add(user)
            db.commit()
            db.refresh(user)

        channel = (
            db.query(Channel)
            .options(selectinload(Channel.videos), selectinload(Channel.metrics))
            .filter(Channel.user_id == user.id)
            .first()
        )
        if channel and channel.videos:
            return user

        channel = Channel(**self.data_service.demo_channel(user.id), last_synced_at=datetime.utcnow())
        db.add(channel)
        db.flush()

        videos: list[Video] = []
        for payload in self.data_service.demo_videos():
            video = Video(channel_id=channel.id, **payload)
            db.add(video)
            db.flush()
            videos.append(video)

        for metric in self.analytics_service.demo_channel_metrics():
            db.add(ChannelMetricDaily(channel_id=channel.id, **metric))

        all_video_metrics = self.analytics_service.demo_video_metrics([video.youtube_video_id for video in videos])
        aggregate_rows: list[dict] = []
        for video in videos:
            series = all_video_metrics[video.youtube_video_id]
            for point in series:
                db.add(VideoMetricDaily(video_id=video.id, **point))
            aggregate_rows.append(
                {
                    "video_id": video.id,
                    "youtube_video_id": video.youtube_video_id,
                    "title": video.title,
                    "published_at": video.published_at,
                    "category": video.category,
                    "total_views": sum(point["views"] for point in series),
                    "avg_ctr_proxy": round(mean(point["ctr_proxy"] for point in series), 2),
                    "avg_engagement_rate": round(mean(point["engagement_rate"] for point in series), 2),
                    "watch_time_hours": round(sum(point["estimated_watch_time"] for point in series) / 60, 1),
                }
            )

        recommendations = self.recommendation_service.build_recommendations(aggregate_rows)
        for video in videos:
            for item in recommendations[video.youtube_video_id]:
                db.add(Recommendation(video_id=video.id, **item))

        db.add(SyncLog(user_id=user.id, status="success", endpoint_called="POST /channels/sync", error_message="Demo sync completed"))
        db.commit()
        return user

    def sync_channel(self, db: Session) -> dict:
        user = self.ensure_demo_dataset(db)
        channel = db.query(Channel).filter(Channel.user_id == user.id).first()
        if channel:
            channel.last_synced_at = datetime.utcnow()
        db.add(SyncLog(user_id=user.id, status="success", endpoint_called="youtube.sync", error_message="Sync completed"))
        db.commit()
        return {"status": "ok", "channel_id": channel.id if channel else None}
