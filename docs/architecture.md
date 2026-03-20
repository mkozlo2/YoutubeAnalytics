# Architecture

## System Overview

The platform uses a React dashboard frontend and a FastAPI backend connected to PostgreSQL.

1. The user starts Google OAuth from the frontend.
2. FastAPI exchanges the auth code for tokens and stores encrypted credentials.
3. Sync services fetch channel metadata from the YouTube Data API and report metrics from the YouTube Analytics API.
4. The ETL layer normalizes results into channel, video, daily metric, recommendation, and sync log tables.
5. The frontend renders overview, trends, video analysis, and debug health pages.

## Design Principles

- Demo-friendly: the app works without live credentials through seeded sample data
- Production-aligned: service boundaries match real OAuth and YouTube API integrations
- Quota-aware: expensive API methods are isolated and surfaced in the debug view
- Partner-focused: sync logs, auth status, freshness, and operational health are first-class
