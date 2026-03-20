import { useParams } from "react-router-dom";

import { fetchVideo } from "../api/videosApi";
import { PerformanceLineChart } from "../components/charts/PerformanceLineChart";
import { LoadingPanel } from "../components/common/LoadingPanel";
import { useApi } from "../hooks/useApi";
import { formatDate } from "../utils/format";

export function VideoDetailPage() {
  const { videoId = "1" } = useParams();
  const { data, loading } = useApi(() => fetchVideo(videoId), [videoId]);

  if (loading || !data) {
    return <LoadingPanel label="Loading video analysis..." />;
  }

  return (
    <div className="space-y-6">
      <section className="rounded-[2rem] border border-white/60 bg-white/85 p-8 shadow-panel">
        <p className="text-sm uppercase tracking-[0.28em] text-slate-500">{data.category}</p>
        <h1 className="mt-3 font-display text-4xl text-ink">{data.title}</h1>
        <p className="mt-4 max-w-3xl text-slate-600">{data.description}</p>
        <div className="mt-6 flex flex-wrap gap-3">
          <span className="rounded-full bg-slate-100 px-4 py-2 text-sm font-semibold text-slate-700">
            Published {formatDate(data.published_at)}
          </span>
          <span className="rounded-full bg-slate-100 px-4 py-2 text-sm font-semibold text-slate-700">{data.duration}</span>
          {data.tags.map((tag) => (
            <span key={tag} className="rounded-full bg-coral/10 px-4 py-2 text-sm font-semibold text-coral">
              {tag}
            </span>
          ))}
        </div>
      </section>

      <section className="grid gap-6 xl:grid-cols-[1.2fr,0.8fr]">
        <PerformanceLineChart
          data={data.daily_metrics.map((metric) => ({
            date: metric.date,
            views: metric.views,
            watch_time: metric.estimated_watch_time,
            engagement_rate: metric.engagement_rate,
          }))}
        />
        <div className="rounded-[2rem] border border-white/60 bg-white/85 p-6 shadow-panel">
          <h3 className="font-display text-xl text-ink">Optimization Suggestions</h3>
          <div className="mt-4 space-y-3">
            {data.recommendations.map((item) => (
              <div key={item.id} className="rounded-2xl bg-slate-50 p-4">
                <div className="flex items-center justify-between gap-3">
                  <span className="text-xs font-semibold uppercase tracking-[0.24em] text-slate-500">{item.type}</span>
                  <span className="rounded-full bg-ink px-3 py-1 text-xs font-semibold text-white">{item.priority}</span>
                </div>
                <p className="mt-3 text-sm text-slate-700">{item.message}</p>
              </div>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
}
