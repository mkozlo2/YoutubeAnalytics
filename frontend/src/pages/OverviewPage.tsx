import { fetchOverview } from "../api/analyticsApi";
import { fetchChannel } from "../api/channelApi";
import { LoadingPanel } from "../components/common/LoadingPanel";
import { MetricCard } from "../components/common/MetricCard";
import { VideoTable } from "../components/dashboard/VideoTable";
import { useApi } from "../hooks/useApi";
import { formatCompactNumber, formatPercent } from "../utils/format";

export function OverviewPage() {
  const overview = useApi(fetchOverview);
  const channel = useApi(fetchChannel);

  if (overview.loading || channel.loading || !overview.data || !channel.data) {
    return <LoadingPanel label="Loading partner overview..." />;
  }

  return (
    <div className="space-y-6">
      <section className="grid gap-4 lg:grid-cols-[1.3fr,0.7fr]">
        <div className="rounded-[2rem] border border-white/60 bg-ink p-8 text-white shadow-panel">
          <p className="text-sm uppercase tracking-[0.3em] text-teal">Channel snapshot</p>
          <h1 className="mt-3 font-display text-4xl">{channel.data.channel_title}</h1>
          <p className="mt-3 max-w-2xl text-slate-300">
            Built for partner teams who need operational clarity, not just vanity metrics. The dashboard blends performance signals with sync and integration readiness.
          </p>
          <div className="mt-8 grid gap-4 sm:grid-cols-3">
            <div>
              <p className="text-sm text-slate-400">Subscribers</p>
              <p className="mt-2 font-display text-3xl">{formatCompactNumber(channel.data.subscriber_count)}</p>
            </div>
            <div>
              <p className="text-sm text-slate-400">Lifetime views</p>
              <p className="mt-2 font-display text-3xl">{formatCompactNumber(channel.data.view_count)}</p>
            </div>
            <div>
              <p className="text-sm text-slate-400">Sync state</p>
              <p className="mt-2 font-display text-2xl">Healthy</p>
            </div>
          </div>
        </div>
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-1">
          <MetricCard label="Total videos" value={String(overview.data.total_videos)} hint="Tracked in the active content library." />
          <MetricCard label="Avg engagement" value={formatPercent(overview.data.avg_engagement_rate)} hint="Derived from likes and comments per view." />
        </div>
      </section>

      <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        <MetricCard label="Synced views" value={formatCompactNumber(overview.data.total_views)} hint="Aggregated across recent daily metric rows." />
        <MetricCard label="Watch time" value={`${formatCompactNumber(Math.round(overview.data.total_watch_time_hours))} hrs`} hint="Estimated watch time converted to hours." />
        <MetricCard label="Upload cadence" value={`${overview.data.upload_frequency_days} days`} hint="Average days between recent uploads." />
        <MetricCard label="Subscriber base" value={formatCompactNumber(overview.data.subscriber_count)} hint="Pulled from channel snapshot." />
      </section>

      <section className="grid gap-6 xl:grid-cols-2">
        <VideoTable title="Top-performing videos" videos={overview.data.top_videos} />
        <VideoTable title="Videos needing attention" videos={overview.data.weakest_videos} />
      </section>
    </div>
  );
}
