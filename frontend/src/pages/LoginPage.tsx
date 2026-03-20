import { Link } from "react-router-dom";

import { getLoginUrl } from "../api/authApi";

export function LoginPage() {
  return (
    <div className="flex min-h-screen items-center justify-center bg-[linear-gradient(135deg,_#08111f_0%,_#0f2942_35%,_#113b48_100%)] px-4 py-10 text-white">
      <div className="w-full max-w-5xl rounded-[2.5rem] border border-white/10 bg-white/10 p-8 shadow-2xl backdrop-blur sm:p-12">
        <p className="text-sm uppercase tracking-[0.35em] text-teal">Partner-grade reporting</p>
        <h1 className="mt-4 max-w-3xl font-display text-4xl leading-tight sm:text-6xl">
          The operating system for YouTube analytics, sync health, and optimization decisions.
        </h1>
        <p className="mt-6 max-w-2xl text-lg text-slate-200">
          Connect a channel, sync performance data, detect weak videos, and give partner teams a cleaner way to diagnose OAuth and API issues.
        </p>
        <div className="mt-8 flex flex-wrap gap-4">
          <a
            href={getLoginUrl()}
            className="rounded-full bg-coral px-6 py-3 font-semibold text-white transition hover:bg-[#ff633d]"
          >
            Connect Google OAuth
          </a>
          <Link
            to="/overview"
            className="rounded-full border border-white/20 px-6 py-3 font-semibold text-white transition hover:bg-white/10"
          >
            Explore demo workspace
          </Link>
        </div>
      </div>
    </div>
  );
}
