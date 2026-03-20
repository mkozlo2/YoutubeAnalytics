from datetime import datetime, timedelta

import httpx
from fastapi import HTTPException


class YouTubeDataService:
    base_url = "https://www.googleapis.com/youtube/v3"

    async def fetch_channel(self, access_token: str) -> dict:
        response = await self._get(
            "/channels",
            access_token,
            {
                "part": "snippet,statistics,contentDetails",
                "mine": "true",
            },
        )
        items = response.get("items", [])
        if not items:
            raise HTTPException(status_code=404, detail="No YouTube channel was found for this Google account.")
        channel = items[0]
        return {
            "youtube_channel_id": channel["id"],
            "channel_title": channel["snippet"]["title"],
            "subscriber_count": int(channel["statistics"].get("subscriberCount", 0)),
            "video_count": int(channel["statistics"].get("videoCount", 0)),
            "view_count": int(channel["statistics"].get("viewCount", 0)),
            "uploads_playlist_id": channel["contentDetails"]["relatedPlaylists"]["uploads"],
        }

    async def fetch_recent_videos(self, access_token: str, uploads_playlist_id: str, limit: int = 12) -> list[dict]:
        playlist_items = await self._get(
            "/playlistItems",
            access_token,
            {
                "part": "contentDetails",
                "playlistId": uploads_playlist_id,
                "maxResults": min(limit, 50),
            },
        )
        video_ids = [item["contentDetails"]["videoId"] for item in playlist_items.get("items", [])]
        if not video_ids:
            return []
        videos_response = await self._get(
            "/videos",
            access_token,
            {
                "part": "snippet,contentDetails,statistics",
                "id": ",".join(video_ids),
                "maxResults": len(video_ids),
            },
        )
        videos = []
        for item in videos_response.get("items", []):
            videos.append(
                {
                    "youtube_video_id": item["id"],
                    "title": item["snippet"]["title"],
                    "description": item["snippet"].get("description", ""),
                    "published_at": datetime.fromisoformat(item["snippet"]["publishedAt"].replace("Z", "+00:00")).replace(tzinfo=None),
                    "duration": item["contentDetails"].get("duration", "PT0M"),
                    "tags": ",".join(item["snippet"].get("tags", [])),
                    "category": item["snippet"].get("categoryId", "General"),
                    "lifetime_views": int(item["statistics"].get("viewCount", 0)),
                    "lifetime_likes": int(item["statistics"].get("likeCount", 0)),
                    "lifetime_comments": int(item["statistics"].get("commentCount", 0)),
                }
            )
        videos.sort(key=lambda item: item["published_at"], reverse=True)
        return videos

    async def _get(self, path: str, access_token: str, params: dict) -> dict:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.get(
                f"{self.base_url}{path}",
                params=params,
                headers={"Authorization": f"Bearer {access_token}"},
            )
        if response.is_error:
            raise HTTPException(status_code=400, detail=f"YouTube Data API request failed: {response.text}")
        return response.json()

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
                "lifetime_views": 284000,
                "lifetime_likes": 14300,
                "lifetime_comments": 910,
            },
            {
                "youtube_video_id": "vid_ops_002",
                "title": "Weekly Partner Ops Review: What Actually Matters",
                "description": "Metrics and habits for media teams managing multiple channels.",
                "published_at": now - timedelta(days=30),
                "duration": "PT9M50S",
                "tags": "partner ops,dashboard,media company",
                "category": "Business",
                "lifetime_views": 192000,
                "lifetime_likes": 9800,
                "lifetime_comments": 605,
            },
            {
                "youtube_video_id": "vid_title_003",
                "title": "YouTube Tips for Everyone",
                "description": "Broad advice with low differentiation.",
                "published_at": now - timedelta(days=17),
                "duration": "PT8M12S",
                "tags": "youtube tips,creators",
                "category": "Howto",
                "lifetime_views": 64000,
                "lifetime_likes": 2100,
                "lifetime_comments": 150,
            },
            {
                "youtube_video_id": "vid_weekend_004",
                "title": "Weekend Upload Test: Do Saturday Videos Still Work?",
                "description": "Testing weekend posting strategy against weekday uploads.",
                "published_at": now - timedelta(days=8),
                "duration": "PT11M40S",
                "tags": "upload timing,weekend strategy",
                "category": "Education",
                "lifetime_views": 118000,
                "lifetime_likes": 6400,
                "lifetime_comments": 410,
            },
        ]
