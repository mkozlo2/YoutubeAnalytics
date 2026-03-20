from datetime import date, timedelta

import httpx
from fastapi import HTTPException


class YouTubeAnalyticsService:
    base_url = "https://youtubeanalytics.googleapis.com/v2/reports"

    async def fetch_channel_metrics(self, access_token: str, days: int = 28) -> list[dict]:
        start_date = date.today() - timedelta(days=days - 1)
        response = await self._query(
            access_token,
            {
                "ids": "channel==MINE",
                "startDate": start_date.isoformat(),
                "endDate": date.today().isoformat(),
                "metrics": "views,estimatedMinutesWatched,subscribersGained,subscribersLost",
                "dimensions": "day",
                "sort": "day",
            },
        )
        return [
            {
                "date": date.fromisoformat(row[0]),
                "views": int(row[1]),
                "watch_time": int(row[2]),
                "subscribers_gained": int(row[3]),
                "subscribers_lost": int(row[4]),
            }
            for row in response.get("rows", [])
        ]

    async def fetch_video_metrics(self, access_token: str, video_ids: list[str], days: int = 28) -> dict[str, list[dict]]:
        start_date = date.today() - timedelta(days=days - 1)
        metrics: dict[str, list[dict]] = {}
        for video_id in video_ids:
            response = await self._query(
                access_token,
                {
                    "ids": "channel==MINE",
                    "startDate": start_date.isoformat(),
                    "endDate": date.today().isoformat(),
                    "metrics": "views,likes,comments,estimatedMinutesWatched",
                    "dimensions": "day",
                    "sort": "day",
                    "filters": f"video=={video_id}",
                },
            )
            series = []
            rows = response.get("rows", [])
            for row in rows:
                views = int(row[1])
                likes = int(row[2])
                comments = int(row[3])
                watch_time = int(row[4])
                series.append(
                    {
                        "date": date.fromisoformat(row[0]),
                        "views": views,
                        "likes": likes,
                        "comments": comments,
                        "estimated_watch_time": watch_time,
                        "ctr_proxy": round(min(12.0, max(2.0, 4.5 + (likes / max(views, 1)) * 100)), 2),
                        "engagement_rate": round(((likes + comments) / max(views, 1)) * 100, 2),
                    }
                )
            metrics[video_id] = series
        return metrics

    async def _query(self, access_token: str, params: dict) -> dict:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.get(
                self.base_url,
                params=params,
                headers={"Authorization": f"Bearer {access_token}"},
            )
        if response.is_error:
            raise HTTPException(status_code=400, detail=f"YouTube Analytics API request failed: {response.text}")
        return response.json()

    def demo_channel_metrics(self, days: int = 14) -> list[dict]:
        today = date.today()
        metrics: list[dict] = []
        for offset in range(days):
            day = today - timedelta(days=days - offset - 1)
            views = 10200 + offset * 320 + (offset % 3) * 400
            metrics.append(
                {
                    "date": day,
                    "views": views,
                    "watch_time": int(views * 4.2),
                    "subscribers_gained": 85 + offset * 2,
                    "subscribers_lost": 11 + (offset % 4),
                }
            )
        return metrics

    def demo_video_metrics(self, video_ids: list[str], days: int = 14) -> dict[str, list[dict]]:
        today = date.today()
        base_views = {
            "vid_growth_001": 2900,
            "vid_ops_002": 2400,
            "vid_title_003": 1100,
            "vid_weekend_004": 2100,
        }
        metrics: dict[str, list[dict]] = {}
        for video_id in video_ids:
            series = []
            for offset in range(days):
                day = today - timedelta(days=days - offset - 1)
                views = base_views.get(video_id, 1500) + offset * 90 - (60 if video_id == "vid_title_003" else 0)
                likes = max(int(views * 0.06), 1)
                comments = max(int(views * 0.008), 1)
                engagement = round(((likes + comments) / max(views, 1)) * 100, 2)
                ctr_proxy = round(4.4 if video_id == "vid_title_003" else 6.1 + offset * 0.02, 2)
                series.append(
                    {
                        "date": day,
                        "views": views,
                        "likes": likes,
                        "comments": comments,
                        "estimated_watch_time": int(views * (3.4 if video_id == "vid_title_003" else 5.2)),
                        "ctr_proxy": ctr_proxy,
                        "engagement_rate": engagement,
                    }
                )
            metrics[video_id] = series
        return metrics
