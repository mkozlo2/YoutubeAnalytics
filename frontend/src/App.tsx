import { Navigate, Route, Routes } from "react-router-dom";

import { AppShell } from "./components/layout/AppShell";
import { DebugPage } from "./pages/DebugPage";
import { LoginPage } from "./pages/LoginPage";
import { OverviewPage } from "./pages/OverviewPage";
import { TrendsPage } from "./pages/TrendsPage";
import { VideoDetailPage } from "./pages/VideoDetailPage";

function DashboardRoutes() {
  return (
    <AppShell>
      <Routes>
        <Route path="/overview" element={<OverviewPage />} />
        <Route path="/trends" element={<TrendsPage />} />
        <Route path="/videos/:videoId" element={<VideoDetailPage />} />
        <Route path="/debug" element={<DebugPage />} />
        <Route path="*" element={<Navigate to="/overview" replace />} />
      </Routes>
    </AppShell>
  );
}

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<LoginPage />} />
      <Route path="/*" element={<DashboardRoutes />} />
    </Routes>
  );
}
