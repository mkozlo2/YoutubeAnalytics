export function LoadingPanel({ label = "Loading dashboard..." }: { label?: string }) {
  return (
    <div className="rounded-3xl border border-white/50 bg-white/70 p-8 text-slate-700 shadow-panel backdrop-blur">
      <div className="h-2 w-24 animate-pulse rounded-full bg-coral/60" />
      <p className="mt-4 text-sm">{label}</p>
    </div>
  );
}
