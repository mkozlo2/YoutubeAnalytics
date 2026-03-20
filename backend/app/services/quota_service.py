class QuotaService:
    DAILY_LIMIT = 10_000

    def summary(self) -> dict:
        used = 421
        return {
            "daily_limit": self.DAILY_LIMIT,
            "estimated_used": used,
            "remaining": self.DAILY_LIMIT - used,
            "expensive_calls": [
                {"endpoint": "search.list", "cost": 100, "reason": "Avoided in sync path"},
                {"endpoint": "videos.list", "cost": 1, "reason": "Used for batched metadata fetches"},
                {"endpoint": "reports.query", "cost": 1, "reason": "Used for custom analytics reports"},
            ],
            "recommendations": [
                "Prefer uploads playlist traversal over search-based discovery.",
                "Cache channel metadata and only refresh deltas on demand.",
                "Batch video metadata requests in groups of up to 50 IDs.",
            ],
        }
