from datetime import datetime
from statistics import mean

from fastapi import HTTPException
from sqlalchemy.orm import Session, selectinload

from app.core.auth import get_valid_access_token
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
            video = Video(
                channel_id=channel.id,
                youtube_video_id=payload["youtube_video_id"],
                title=payload["title"],
                description=payload["description"],
                published_at=payload["published_at"],
                duration=payload["duration"],
                tags=payload["tags"],
                category=payload["category"],
            )
            db.add(video)
            db.flush()
            videos.append(video)

        for metric in self.analytics_service.demo_channel_metrics():
            db.add(ChannelMetricDaily(channel_id=channel.id, **metric))

        all_video_metrics = self.analytics_service.demo_video_metrics([video.youtube_video_id for video in videos])
        aggregate_rows = self._persist_video_metrics(db, videos, all_video_metrics)
        self._persist_recommendations(db, videos, aggregate_rows)

        db.add(SyncLog(user_id=user.id, status="success", endpoint_called="demo.sync", error_message="Demo sync completed"))
        db.commit()
        return user

    async def sync_channel(self, db: Session, user: User) -> dict:
        if user.email == "demo@partnerplatform.dev":
            self.ensure_demo_dataset(db)
            db.add(
                SyncLog(
                    user_id=user.id,
                    status="success",
                    endpoint_called="demo.sync",
                    error_message="Demo data refreshed.",
                )
            )
            db.commit()
            channel = db.query(Channel).filter(Channel.user_id == user.id).first()
            return {"status": "ok", "channel_id": channel.id if channel else None, "mode": "demo"}
        try:
            access_token = await get_valid_access_token(user, db)
            channel_payload = await self.data_service.fetch_channel(access_token)
            videos_payload = await self.data_service.fetch_recent_videos(access_token, channel_payload["uploads_playlist_id"])
            if not videos_payload:
                raise HTTPException(status_code=400, detail="No recent uploaded videos were found on the connected channel.")
            analytics_mode = "live"
            try:
                channel_metrics = await self.analytics_service.fetch_channel_metrics(access_token)
                video_metrics = await self.analytics_service.fetch_video_metrics(
                    access_token,
                    [video["youtube_video_id"] for video in videos_payload],
                )
            except HTTPException as exc:
                analytics_mode = "metadata-fallback"
                channel_metrics = []
                video_metrics = {}
                db.add(
                    SyncLog(
                        user_id=user.id,
                        status="warning",
                        endpoint_called="youtube.analytics",
                        error_message=f"Analytics API unavailable, using metadata fallback: {exc.detail}",
                    )
                )
            channel = self._upsert_channel(db, user, channel_payload)
            videos = self._replace_videos(db, channel, videos_payload)
            self._replace_channel_metrics(db, channel, channel_metrics)
            aggregate_rows = self._persist_video_metrics(db, videos, video_metrics, videos_payload)
            self._persist_recommendations(db, videos, aggregate_rows)
            channel.last_synced_at = datetime.utcnow()
            db.add(
                SyncLog(
                    user_id=user.id,
                    status="success",
                    endpoint_called="youtube.sync",
                    error_message=f"Synced {len(videos)} videos from YouTube using {analytics_mode}.",
                )
            )
            db.commit()
            return {"status": "ok", "channel_id": channel.id, "mode": analytics_mode}
        except HTTPException as exc:
            db.add(
                SyncLog(
                    user_id=user.id,
                    status="error",
                    endpoint_called="youtube.sync",
                    error_message=exc.detail,
                )
            )
            db.commit()
            raise

    def _upsert_channel(self, db: Session, user: User, payload: dict) -> Channel:
        channel = db.query(Channel).filter(Channel.user_id == user.id).first()
        if not channel:
            channel = Channel(user_id=user.id, youtube_channel_id=payload["youtube_channel_id"], channel_title=payload["channel_title"])
            db.add(channel)
            db.flush()
        channel.youtube_channel_id = payload["youtube_channel_id"]
        channel.channel_title = payload["channel_title"]
        channel.subscriber_count = payload["subscriber_count"]
        channel.video_count = payload["video_count"]
        channel.view_count = payload["view_count"]
        return channel

    def _replace_videos(self, db: Session, channel: Channel, videos_payload: list[dict]) -> list[Video]:
        existing_video_ids = [video_id for (video_id,) in db.query(Video.id).filter(Video.channel_id == channel.id).all()]
        if existing_video_ids:
            db.query(Recommendation).filter(Recommendation.video_id.in_(existing_video_ids)).delete(synchronize_session=False)
            db.query(VideoMetricDaily).filter(VideoMetricDaily.video_id.in_(existing_video_ids)).delete(synchronize_session=False)
        db.query(Video).filter(Video.channel_id == channel.id).delete(synchronize_session=False)
        db.flush()

        videos: list[Video] = []
        for payload in videos_payload:
            video = Video(
                channel_id=channel.id,
                youtube_video_id=payload["youtube_video_id"],
                title=payload["title"],
                description=payload["description"],
                published_at=payload["published_at"],
                duration=payload["duration"],
                tags=payload["tags"],
                category=payload["category"],
            )
            db.add(video)
            db.flush()
            videos.append(video)
        return videos

    def _replace_channel_metrics(self, db: Session, channel: Channel, metrics: list[dict]) -> None:
        db.query(ChannelMetricDaily).filter(ChannelMetricDaily.channel_id == channel.id).delete(synchronize_session=False)
        for metric in metrics:
            db.add(ChannelMetricDaily(channel_id=channel.id, **metric))

    def _persist_video_metrics(
        self,
        db: Session,
        videos: list[Video],
        metrics_by_video_id: dict[str, list[dict]],
        source_payloads: list[dict] | None = None,
    ) -> list[dict]:
        lifetime_lookup = {item["youtube_video_id"]: item for item in (source_payloads or [])}
        aggregate_rows: list[dict] = []
        for video in videos:
            series = metrics_by_video_id.get(video.youtube_video_id, [])
            if not series:
                lifetime = lifetime_lookup.get(video.youtube_video_id, {})
                synthetic_views = max(1, int(lifetime.get("lifetime_views", 0)))
                synthetic_likes = max(1, int(lifetime.get("lifetime_likes", 0)))
                synthetic_comments = max(1, int(lifetime.get("lifetime_comments", 0)))
                series = [
                    {
                        "date": datetime.utcnow().date(),
                        "views": synthetic_views,
                        "likes": synthetic_likes,
                        "comments": synthetic_comments,
                        "estimated_watch_time": max(60, synthetic_views * 4),
                        "ctr_proxy": round(min(12.0, max(2.5, 4.8 + (synthetic_likes / max(synthetic_views, 1)) * 100)), 2),
                        "engagement_rate": round(((synthetic_likes + synthetic_comments) / max(synthetic_views, 1)) * 100, 2),
                    }
                ]
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
        return aggregate_rows

    def _persist_recommendations(self, db: Session, videos: list[Video], aggregate_rows: list[dict]) -> None:
        recommendations = self.recommendation_service.build_recommendations(aggregate_rows)
        for video in videos:
            for item in recommendations.get(video.youtube_video_id, []):
                db.add(Recommendation(video_id=video.id, **item))
