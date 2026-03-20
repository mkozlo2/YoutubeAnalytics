from statistics import mean


class RecommendationService:
    def build_recommendations(self, videos: list[dict]) -> dict[str, list[dict]]:
        if not videos:
            return {}
        baseline_ctr = mean(video["avg_ctr_proxy"] for video in videos)
        baseline_views = mean(video["total_views"] for video in videos)
        results: dict[str, list[dict]] = {}

        for video in videos:
            items: list[dict] = []
            if video["avg_ctr_proxy"] < baseline_ctr - 0.7:
                items.append(
                    {
                        "type": "title-packaging",
                        "message": "CTR proxy trails the channel baseline. Test a sharper title and more specific thumbnail promise.",
                        "priority": "high",
                    }
                )
            if video["total_views"] < baseline_views * 0.75:
                items.append(
                    {
                        "type": "distribution",
                        "message": "Recent view velocity is below your channel norm. Recut short-form clips and resurface the video in community posts.",
                        "priority": "medium",
                    }
                )
            if "Weekend" in video["title"]:
                items.append(
                    {
                        "type": "timing",
                        "message": "Weekend experiments show solid watch time. Consider repeating this upload window for education content.",
                        "priority": "medium",
                    }
                )
            if not items:
                items.append(
                    {
                        "type": "momentum",
                        "message": "This video is holding above baseline. Reuse its topic framing in the next content sprint.",
                        "priority": "low",
                    }
                )
            results[video["youtube_video_id"]] = items
        return results
