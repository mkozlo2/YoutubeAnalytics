from datetime import datetime, timedelta


class YouTubeDataService:
    def demo_channel(self, user_id: int) -> dict:
        return {
            "user_id": user_id,
            "youtube_channel_id": "UCDEMO123PARTNER",
            "channel_title": "North Star Creator Network",
            "subscriber_count": 187_500,
            "video_count": 48,
            "view_count": 5_420_000,
        }

    def demo_videos(self) -> list[dict]:
        now = datetime.utcnow()
        return [
            {
                "youtube_video_id": "vid_growth_001",
                "title": "How We Doubled Shorts Retention in 30 Days",
                "description": "A breakdown of retention wins for creator ops teams.",
                "published_at": now - timedelta(days=45),
                "duration": "PT12M14S",
                "tags": "youtube growth,retention,shorts,analytics",
                "category": "Education",
            },
            {
                "youtube_video_id": "vid_ops_002",
                "title": "Weekly Partner Ops Review: What Actually Matters",
                "description": "Metrics and habits for media teams managing multiple channels.",
                "published_at": now - timedelta(days=30),
                "duration": "PT9M50S",
                "tags": "partner ops,dashboard,media company",
                "category": "Business",
            },
            {
                "youtube_video_id": "vid_title_003",
                "title": "YouTube Tips for Everyone",
                "description": "Broad advice with low differentiation.",
                "published_at": now - timedelta(days=17),
                "duration": "PT8M12S",
                "tags": "youtube tips,creators",
                "category": "Howto",
            },
            {
                "youtube_video_id": "vid_weekend_004",
                "title": "Weekend Upload Test: Do Saturday Videos Still Work?",
                "description": "Testing weekend posting strategy against weekday uploads.",
                "published_at": now - timedelta(days=8),
                "duration": "PT11M40S",
                "tags": "upload timing,weekend strategy",
                "category": "Education",
            },
        ]
