import { useEffect, useState } from "react";
import {
  Package,
  AlertTriangle,
  CheckCircle,
  Activity,
  RefreshCw,
} from "lucide-react";
import {
  getAnalyticsSummary,
  getAnalyticsBreakdown,
  getDecisionAnalytics,
} from "../services/api";

function Dashboard() {
  const [summary, setSummary] = useState(null);
  const [breakdown, setBreakdown] = useState(null);
  const [decisionAnalytics, setDecisionAnalytics] = useState(null);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const loadDashboard = async () => {
    try {
      setLoading(true);
      setError("");

      const [summaryData, breakdownData, decisionData] =
        await Promise.all([
          getAnalyticsSummary(),
          getAnalyticsBreakdown(),
          getDecisionAnalytics(),
        ]);

      setSummary(summaryData);
      setBreakdown(breakdownData);
      setDecisionAnalytics(decisionData);
    } catch (err) {
      console.error("Dashboard loading error:", err);

      setError(
        err.response?.data?.detail ||
          "Unable to connect to the SupplyPrescript backend."
      );
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadDashboard();
  }, []);

  if (loading) {
    return (
      <div className="page-container">
        <div className="page-header">
          <div>
            <h2>Supply Chain Dashboard</h2>
            <p>Loading operational analytics...</p>
          </div>
        </div>

        <div className="loading-state">
          <RefreshCw className="loading-icon" size={28} />
          <p>Loading dashboard data...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="page-container">
      <div className="page-header">
        <div>
          <h2>Supply Chain Dashboard</h2>
          <p>
            Monitor shipment risk, disruptions, and closed-loop decisions.
          </p>
        </div>

        <button className="refresh-button" onClick={loadDashboard}>
          <RefreshCw size={17} />
          Refresh
        </button>
      </div>

      {error && (
        <div className="error-banner">
          <AlertTriangle size={20} />
          <div>
            <strong>Backend connection unavailable</strong>
            <p>{error}</p>
          </div>
        </div>
      )}

      <div className="stats-grid">
        <StatCard
          title="Total Shipments"
          value={summary?.total_shipments ?? 0}
          icon={<Package size={22} />}
        />

        <StatCard
          title="Delayed Shipments"
          value={summary?.delayed_shipments ?? 0}
          icon={<AlertTriangle size={22} />}
        />

        <StatCard
          title="On-Time Shipments"
          value={summary?.on_time_shipments ?? 0}
          icon={<CheckCircle size={22} />}
        />

        <StatCard
          title="Average Risk"
          value={
            summary?.average_delay_probability !== undefined
              ? `${(summary.average_delay_probability * 100).toFixed(1)}%`
              : "0%"
          }
          icon={<Activity size={22} />}
        />
      </div>

      <div className="dashboard-grid">
        <section className="dashboard-card">
          <div className="card-header">
            <div>
              <h3>Risk Overview</h3>
              <p>Current shipment prediction distribution</p>
            </div>
          </div>

          {breakdown ? (
            <div className="breakdown-list">
              {Object.entries(breakdown).map(([key, value]) => (
                <div className="breakdown-row" key={key}>
                  <span>{formatLabel(key)}</span>
                  <strong>{formatValue(value)}</strong>
                </div>
              ))}
            </div>
          ) : (
            <div className="empty-state">
              No breakdown data available.
            </div>
          )}
        </section>

        <section className="dashboard-card">
          <div className="card-header">
            <div>
              <h3>Decision Performance</h3>
              <p>Closed-loop operational outcomes</p>
            </div>
          </div>

          {decisionAnalytics ? (
            <div className="decision-metrics">
              <Metric
                label="Total Decisions"
                value={decisionAnalytics.total_decisions ?? 0}
              />

              <Metric
                label="Executed"
                value={decisionAnalytics.executed_decisions ?? 0}
              />

              <Metric
                label="Evaluated"
                value={decisionAnalytics.evaluated_decisions ?? 0}
              />

              <Metric
                label="Better Outcomes"
                value={decisionAnalytics.better_outcomes ?? 0}
              />

              <Metric
                label="Worse Outcomes"
                value={decisionAnalytics.worse_outcomes ?? 0}
              />

              <Metric
                label="Mixed Outcomes"
                value={decisionAnalytics.mixed_outcomes ?? 0}
              />
            </div>
          ) : (
            <div className="empty-state">
              No decision analytics available.
            </div>
          )}
        </section>
      </div>
    </div>
  );
}

function StatCard({ title, value, icon }) {
  return (
    <div className="stat-card">
      <div className="stat-icon">{icon}</div>

      <div>
        <p>{title}</p>
        <h3>{value}</h3>
      </div>
    </div>
  );
}

function Metric({ label, value }) {
  return (
    <div className="metric">
      <span>{label}</span>
      <strong>{value}</strong>
    </div>
  );
}

function formatLabel(value) {
  return value
    .replaceAll("_", " ")
    .replace(/\b\w/g, (letter) => letter.toUpperCase());
}

function formatValue(value) {
  if (typeof value === "number") {
    return value.toLocaleString();
  }

  return String(value);
}

export default Dashboard;