import { fetchTrends } from "../api/analyticsApi";
import { CategoryBarChart } from "../components/charts/CategoryBarChart";
import { PerformanceLineChart } from "../components/charts/PerformanceLineChart";
import { LoadingPanel } from "../components/common/LoadingPanel";
import { useApi } from "../hooks/useApi";

export function TrendsPage() {
  const { data, loading } = useApi(fetchTrends);

  if (loading || !data) {
    return <LoadingPanel label="Loading trends..." />;
  }

  return (
    <div className="grid gap-6 xl:grid-cols-[1.4fr,0.6fr]">
      <PerformanceLineChart data={data.series} />
      <div className="space-y-6">
        <CategoryBarChart data={data.by_category} />
        <div className="rounded-[2rem] border border-white/60 bg-white/85 p-6 shadow-panel">
          <h3 className="font-display text-xl text-ink">Upload Day Pattern</h3>
          <div className="mt-4 space-y-3">
            {data.by_upload_day.map((item) => (
              <div key={item.day} className="flex items-center justify-between rounded-2xl bg-slate-50 px-4 py-3">
                <span className="font-medium text-slate-700">{item.day}</span>
                <span className="rounded-full bg-ink px-3 py-1 text-xs font-semibold text-white">{item.videos} videos</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
