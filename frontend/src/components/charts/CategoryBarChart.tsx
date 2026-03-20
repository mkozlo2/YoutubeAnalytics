import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

export function CategoryBarChart({ data }: { data: Array<{ category: string; videos: number }> }) {
  return (
    <div className="rounded-[2rem] border border-white/60 bg-white/85 p-6 shadow-panel">
      <h3 className="font-display text-xl text-ink">Content Mix</h3>
      <p className="mb-4 text-sm text-slate-600">Categories represented in the synced library.</p>
      <div className="h-72">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={data}>
            <CartesianGrid strokeDasharray="3 3" stroke="#d8e4f2" />
            <XAxis dataKey="category" stroke="#60758b" />
            <YAxis stroke="#60758b" />
            <Tooltip />
            <Bar dataKey="videos" fill="#f7b500" radius={[12, 12, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
