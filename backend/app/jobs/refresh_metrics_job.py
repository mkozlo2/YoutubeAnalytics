from app.services.sync_service import SyncService


def refresh_metrics_job() -> str:
    service = SyncService()
    return f"{service.__class__.__name__} is ready for scheduler integration."
