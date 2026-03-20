# Schema

## Core Tables

- `users`: application users
- `oauth_tokens`: encrypted Google OAuth credentials
- `channels`: connected YouTube channels
- `videos`: video metadata
- `video_metrics_daily`: daily per-video metrics
- `channel_metrics_daily`: channel rollups
- `recommendations`: optimization findings
- `sync_logs`: sync, quota, and auth diagnostics

## Derived Metrics

- engagement rate
- watch time per view
- rolling average views
- upload cadence gaps
- performance delta vs channel baseline
