import { fetchAuthStatus } from "../api/authApi";
import { fetchQuotaSummary } from "../api/analyticsApi";
import { fetchSyncLogs } from "../api/channelApi";
import { LoadingPanel } from "../components/common/LoadingPanel";
import { useApi } from "../hooks/useApi";

export function DebugPage() {
  const auth = useApi(fetchAuthStatus);
  const quota = useApi(fetchQuotaSummary);
  const logs = useApi(fetchSyncLogs);

  if (auth.loading || quota.loading || logs.loading || !auth.data || !quota.data || !logs.data) {
    return <LoadingPanel label="Loading integration health..." />;
  }

  return (
    <div className="grid gap-6 xl:grid-cols-[0.95fr,1.05fr]">
      <div className="space-y-6">
        <div className="rounded-[2rem] border border-white/60 bg-white/85 p-6 shadow-panel">
          <h2 className="font-display text-2xl text-ink">Auth Status</h2>
          <div className="mt-4 grid gap-4 sm:grid-cols-2">
            <div className="rounded-2xl bg-slate-50 p-4">
              <p className="text-xs uppercase tracking-[0.24em] text-slate-500">Connected</p>
              <p className="mt-2 text-lg font-semibold text-slate-800">{auth.data.connected ? "Yes" : "No"}</p>
            </div>
            <div className="rounded-2xl bg-slate-50 p-4">
              <p className="text-xs uppercase tracking-[0.24em] text-slate-500">Demo mode</p>
              <p className="mt-2 text-lg font-semibold text-slate-800">{auth.data.demo_mode ? "Enabled" : "Disabled"}</p>
            </div>
          </div>
          <div className="mt-5 space-y-2">
            {auth.data.issues.map((issue) => (
              <div key={issue} className="rounded-2xl border border-amber-200 bg-amber-50 px-4 py-3 text-sm text-amber-900">
                {issue}
              </div>
            ))}
          </div>
        </div>

        <div className="rounded-[2rem] border border-white/60 bg-white/85 p-6 shadow-panel">
          <h2 className="font-display text-2xl text-ink">Quota Summary</h2>
          <p className="mt-2 text-sm text-slate-600">
            Estimated usage: {quota.data.estimated_used} / {quota.data.daily_limit} units
          </p>
          <div className="mt-5 space-y-3">
            {quota.data.expensive_calls.map((item) => (
              <div key={item.endpoint} className="rounded-2xl bg-slate-50 p-4">
                <div className="flex items-center justify-between gap-3">
                  <span className="font-semibold text-slate-800">{item.endpoint}</span>
                  <span className="rounded-full bg-gold/20 px-3 py-1 text-xs font-semibold text-slate-800">
                    {item.cost} units
                  </span>
                </div>
                <p className="mt-2 text-sm text-slate-600">{item.reason}</p>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="space-y-6">
        <div className="rounded-[2rem] border border-white/60 bg-white/85 p-6 shadow-panel">
          <h2 className="font-display text-2xl text-ink">Sync Logs</h2>
          <div className="mt-4 space-y-3">
            {logs.data.map((log) => (
              <div key={log.id} className="rounded-2xl bg-slate-50 p-4">
                <div className="flex items-center justify-between gap-3">
                  <span className="rounded-full bg-ink px-3 py-1 text-xs font-semibold uppercase tracking-[0.16em] text-white">
                    {log.status}
                  </span>
                  <span className="text-xs text-slate-500">{new Date(log.created_at).toLocaleString()}</span>
                </div>
                <p className="mt-3 font-semibold text-slate-800">{log.endpoint_called}</p>
                <p className="mt-1 text-sm text-slate-600">{log.error_message}</p>
              </div>
            ))}
          </div>
        </div>

        <div className="rounded-[2rem] border border-white/60 bg-white/85 p-6 shadow-panel">
          <h2 className="font-display text-2xl text-ink">Operational Notes</h2>
          <div className="mt-4 space-y-3 text-sm text-slate-700">
            {quota.data.recommendations.map((item) => (
              <div key={item} className="rounded-2xl border border-teal/20 bg-teal/10 px-4 py-3">
                {item}
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
