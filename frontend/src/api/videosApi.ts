import { apiRequest } from "./client";
import type { Recommendation, VideoDetail, VideoSummary } from "../types";

export const fetchVideos = () => apiRequest<VideoSummary[]>("/videos");
export const fetchVideo = (videoId: string) => apiRequest<VideoDetail>(`/videos/${videoId}`);
export const fetchVideoRecommendations = (videoId: string) =>
  apiRequest<Recommendation[]>(`/videos/${videoId}/recommendations`);
