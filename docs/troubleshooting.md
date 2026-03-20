# Troubleshooting

## Common OAuth Failures

- Invalid redirect URI: verify `GOOGLE_REDIRECT_URI`
- Missing scope: confirm YouTube readonly and analytics scopes are requested
- Expired refresh token: prompt the user to reconnect Google auth

## Common API Failures

- Quota exceeded: reduce costly methods, cache metadata, batch `videos.list`
- Channel not found: ensure the authenticated Google account owns or can access the channel
- Empty analytics report: verify date windows and scope permissions

## Demo Mode

When `DEMO_MODE=true`, the backend seeds representative channel/video/metric data and returns working dashboards without live API calls.
