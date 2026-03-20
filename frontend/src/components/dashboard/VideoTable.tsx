import { Link } from "react-router-dom";

import type { VideoSummary } from "../../types";
import { formatCompactNumber, formatDate, formatPercent } from "../../utils/format";

export function VideoTable({ title, videos }: { title: string; videos: VideoSummary[] }) {
  return (
    <div className="rounded-[2rem] border border-white/60 bg-white/85 p-6 shadow-panel">
      <div className="mb-4 flex items-center justify-between">
        <h3 className="font-display text-xl text-ink">{title}</h3>
        <span className="rounded-full bg-slate-100 px-3 py-1 text-xs font-semibold uppercase tracking-[0.2em] text-slate-500">
          {videos.length} videos
        </span>
      </div>
      <div className="overflow-x-auto">
        <table className="min-w-full text-left text-sm">
          <thead>
            <tr className="border-b border-slate-200 text-slate-500">
              <th className="pb-3 font-medium">Video</th>
              <th className="pb-3 font-medium">Published</th>
              <th className="pb-3 font-medium">Views</th>
              <th className="pb-3 font-medium">CTR Proxy</th>
              <th className="pb-3 font-medium">Engagement</th>
            </tr>
          </thead>
          <tbody>
            {videos.map((video) => (
              <tr key={video.id} className="border-b border-slate-100 last:border-0">
                <td className="py-4 pr-6">
                  <Link to={`/videos/${video.id}`} className="font-semibold text-ink hover:text-coral">
                    {video.title}
                  </Link>
                  <p className="mt-1 text-xs uppercase tracking-[0.16em] text-slate-500">{video.category}</p>
                </td>
                <td className="py-4 pr-6 text-slate-600">{formatDate(video.published_at)}</td>
                <td className="py-4 pr-6 text-slate-800">{formatCompactNumber(video.total_views)}</td>
                <td className="py-4 pr-6 text-slate-800">{formatPercent(video.avg_ctr_proxy)}</td>
                <td className="py-4 text-slate-800">{formatPercent(video.avg_engagement_rate)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
