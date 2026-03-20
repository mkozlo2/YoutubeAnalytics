import { apiRequest } from "./client";
import type { Channel, SyncLog } from "../types";

export const fetchChannel = () => apiRequest<Channel>("/channels/me");
export const fetchSyncLogs = () => apiRequest<SyncLog[]>("/debug/sync-logs");
