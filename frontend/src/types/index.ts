export interface Channel {
  id: number;
  youtube_channel_id: string;
  channel_title: string;
  subscriber_count: number;
  video_count: number;
  view_count: number;
  last_synced_at: string | null;
}

export interface VideoSummary {
  id: number;
  youtube_video_id: string;
  title: string;
  published_at: string;
  category: string;
  total_views: number;
  avg_ctr_proxy: number;
  avg_engagement_rate: number;
  watch_time_hours: number;
}

export interface Recommendation {
  id: number;
  type: string;
  message: string;
  priority: string;
  created_at: string;
}

export interface TrendPoint {
  date: string;
  views: number;
  watch_time: number;
  engagement_rate: number;
}

export interface OverviewResponse {
  total_videos: number;
  total_views: number;
  total_watch_time_hours: number;
  subscriber_count: number;
  avg_engagement_rate: number;
  upload_frequency_days: number;
  top_videos: VideoSummary[];
  weakest_videos: VideoSummary[];
}

export interface TrendsResponse {
  series: TrendPoint[];
  by_upload_day: Array<{ day: string; videos: number }>;
  by_category: Array<{ category: string; videos: number }>;
}

export interface VideoDetail extends VideoSummary {
  description: string;
  duration: string;
  tags: string[];
  daily_metrics: Array<{
    date: string;
    views: number;
    likes: number;
    comments: number;
    estimated_watch_time: number;
    ctr_proxy: number;
    engagement_rate: number;
  }>;
  recommendations: Recommendation[];
}

export interface SyncLog {
  id: number;
  status: string;
  endpoint_called: string;
  error_message: string;
  created_at: string;
}

export interface QuotaSummary {
  daily_limit: number;
  estimated_used: number;
  remaining: number;
  expensive_calls: Array<{ endpoint: string; cost: number; reason: string }>;
  recommendations: string[];
}

export interface AuthStatus {
  connected: boolean;
  demo_mode: boolean;
  token_expires_at: string | null;
  scopes: string[];
  refresh_supported: boolean;
  issues: string[];
}
