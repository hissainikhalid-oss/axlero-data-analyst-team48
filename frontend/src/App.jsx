import { BrowserRouter, Routes, Route, NavLink } from "react-router-dom";
import {
  LayoutDashboard,
  Brain,
  Route as RouteIcon,
  ClipboardCheck,
  FileText,
} from "lucide-react";

import Dashboard from "./pages/Dashboard";
import Predictions from "./pages/Predictions";
import Prescriptions from "./pages/Prescriptions";
import Decisions from "./pages/Decisions";
import Reports from "./pages/Reports";

function Sidebar() {
  const navigation = [
    {
      name: "Dashboard",
      path: "/",
      icon: LayoutDashboard,
    },
    {
      name: "Predictions",
      path: "/predictions",
      icon: Brain,
    },
    {
      name: "Prescriptions",
      path: "/prescriptions",
      icon: RouteIcon,
    },
    {
      name: "Decisions",
      path: "/decisions",
      icon: ClipboardCheck,
    },
    {
      name: "Reports",
      path: "/reports",
      icon: FileText,
    },
  ];

  return (
    <aside className="sidebar">
      <div className="brand">
        <div className="brand-icon">SP</div>

        <div>
          <h1>SupplyPrescript</h1>
          <span>Closed-Loop Analytics</span>
        </div>
      </div>

      <nav className="navigation">
        {navigation.map((item) => {
          const Icon = item.icon;

          return (
            <NavLink
              key={item.path}
              to={item.path}
              end={item.path === "/"}
              className={({ isActive }) =>
                `nav-item ${isActive ? "active" : ""}`
              }
            >
              <Icon size={19} />
              <span>{item.name}</span>
            </NavLink>
          );
        })}
      </nav>

      <div className="sidebar-footer">
        <div className="system-status">
          <span className="status-dot"></span>
          <div>
            <strong>System Online</strong>
            <small>FastAPI Connected</small>
          </div>
        </div>
      </div>
    </aside>
  );
}

function App() {
  return (
    <BrowserRouter>
      <div className="app-layout">
        <Sidebar />

        <main className="main-content">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/predictions" element={<Predictions />} />
            <Route path="/prescriptions" element={<Prescriptions />} />
            <Route path="/decisions" element={<Decisions />} />
            <Route path="/reports" element={<Reports />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}

export default App;