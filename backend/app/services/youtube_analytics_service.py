from datetime import date, timedelta


class YouTubeAnalyticsService:
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
