import { CartesianGrid, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import type { TrendPoint } from "../../types";

export function PerformanceLineChart({ data }: { data: TrendPoint[] }) {
  return (
    <div className="rounded-[2rem] border border-white/60 bg-white/85 p-6 shadow-panel">
      <div className="mb-4">
        <h3 className="font-display text-xl text-ink">Performance Over Time</h3>
        <p className="text-sm text-slate-600">Views and watch time trends from the last sync window.</p>
      </div>
      <div className="h-80">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={data}>
            <CartesianGrid strokeDasharray="3 3" stroke="#d8e4f2" />
            <XAxis dataKey="date" stroke="#60758b" />
            <YAxis stroke="#60758b" />
            <Tooltip />
            <Line type="monotone" dataKey="views" stroke="#ff7a59" strokeWidth={3} dot={false} />
            <Line type="monotone" dataKey="watch_time" stroke="#0f766e" strokeWidth={3} dot={false} />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
