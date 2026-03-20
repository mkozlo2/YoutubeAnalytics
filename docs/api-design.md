# API Design

## Auth

- `GET /auth/login`
- `GET /auth/callback`
- `POST /auth/logout`
- `GET /debug/auth-status`

## Channel and Sync

- `GET /channels/me`
- `POST /channels/sync`

## Video and Recommendations

- `GET /videos`
- `GET /videos/{video_id}`
- `GET /videos/{video_id}/recommendations`

## Analytics

- `GET /analytics/overview`
- `GET /analytics/trends`
- `GET /analytics/top-videos`
- `GET /analytics/underperforming-videos`

## Debug

- `GET /debug/sync-logs`
- `GET /debug/quota-summary`
