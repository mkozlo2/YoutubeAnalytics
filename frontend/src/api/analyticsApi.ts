import { apiRequest } from "./client";
import type { OverviewResponse, QuotaSummary, TrendsResponse, VideoSummary } from "../types";

export const fetchOverview = () => apiRequest<OverviewResponse>("/analytics/overview");
export const fetchTrends = () => apiRequest<TrendsResponse>("/analytics/trends");
export const fetchTopVideos = () => apiRequest<VideoSummary[]>("/analytics/top-videos");
export const fetchUnderperformingVideos = () => apiRequest<VideoSummary[]>("/analytics/underperforming-videos");
export const fetchQuotaSummary = () => apiRequest<QuotaSummary>("/debug/quota-summary");
