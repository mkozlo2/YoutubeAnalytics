import type { ReactNode } from "react";
import { Link, NavLink } from "react-router-dom";

const navItems = [
  { to: "/overview", label: "Overview" },
  { to: "/trends", label: "Trends" },
  { to: "/videos/1", label: "Video Analysis" },
  { to: "/debug", label: "Debug Health" },
];

export function AppShell({ children }: { children: ReactNode }) {
  return (
    <div className="min-h-screen bg-[radial-gradient(circle_at_top_left,_rgba(74,215,195,0.28),_transparent_32%),radial-gradient(circle_at_top_right,_rgba(255,122,89,0.22),_transparent_28%),linear-gradient(180deg,_#f8fbff_0%,_#eef5ff_48%,_#fff6ef_100%)] text-slate-900">
      <div className="mx-auto max-w-7xl px-4 py-6 sm:px-6 lg:px-8">
        <header className="mb-8 flex flex-col gap-5 rounded-[2rem] border border-white/60 bg-white/75 p-6 shadow-panel backdrop-blur lg:flex-row lg:items-center lg:justify-between">
          <div>
            <Link to="/overview" className="font-display text-2xl text-ink">
              YouTube Partner Analytics
            </Link>
            <p className="mt-2 max-w-2xl text-sm text-slate-600">
              Built for creators and media partners who want stronger reporting, faster troubleshooting, and clearer optimization signals.
            </p>
          </div>
          <nav className="flex flex-wrap gap-2">
            {navItems.map((item) => (
              <NavLink
                key={item.to}
                to={item.to}
                className={({ isActive }) =>
                  `rounded-full px-4 py-2 text-sm font-semibold transition ${
                    isActive ? "bg-ink text-white" : "bg-slate-100 text-slate-600 hover:bg-slate-200"
                  }`
                }
              >
                {item.label}
              </NavLink>
            ))}
          </nav>
        </header>
        {children}
      </div>
    </div>
  );
}
