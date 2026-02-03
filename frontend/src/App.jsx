import { useEffect, useMemo, useState } from "react";
import {
  BarChart,
  Bar,
  CartesianGrid,
  LineChart,
  Line,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis
} from "recharts";
import StatusTable from "./components/StatusTable.jsx";

const API_BASE = import.meta.env.VITE_API_BASE ?? "http://localhost:8000";

const formatNumber = (value) =>
  Intl.NumberFormat("en-US", { maximumFractionDigits: 2 }).format(value);

export default function App() {
  const [vehicles, setVehicles] = useState([]);
  const [industries, setIndustries] = useState([]);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("Run analysis to load the latest emissions.");

  const fetchData = async () => {
    try {
      const [vehicleRes, industryRes] = await Promise.all([
        fetch(`${API_BASE}/vehicles`),
        fetch(`${API_BASE}/industries`)
      ]);

      if (!vehicleRes.ok || !industryRes.ok) {
        throw new Error("Results unavailable.");
      }

      const [vehicleData, industryData] = await Promise.all([
        vehicleRes.json(),
        industryRes.json()
      ]);

      setVehicles(vehicleData);
      setIndustries(industryData);
      setMessage("Latest emissions loaded.");
    } catch (error) {
      setMessage("Run analysis to generate results.");
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleRunAnalysis = async () => {
    setLoading(true);
    setMessage("Running emission analysis...");

    try {
      const response = await fetch(`${API_BASE}/run-analysis`, {
        method: "POST"
      });

      if (!response.ok) {
        throw new Error("Analysis failed.");
      }

      await fetchData();
    } catch (error) {
      setMessage("Unable to run analysis. Check the backend logs.");
    } finally {
      setLoading(false);
    }
  };

  const topVehicles = useMemo(() => {
    return [...vehicles]
      .sort((a, b) => b.Predicted_CO2 - a.Predicted_CO2)
      .slice(0, 5);
  }, [vehicles]);

  const topIndustries = useMemo(() => {
    return [...industries]
      .sort((a, b) => b.Predicted_CO2 - a.Predicted_CO2)
      .slice(0, 5);
  }, [industries]);

  const trend = useMemo(() => {
    return vehicles.map((item, index) => ({
      ...item,
      Index: index + 1
    }));
  }, [vehicles]);

  const highVehicleCount = vehicles.filter((item) => item.Status === "HIGH").length;
  const highIndustryCount = industries.filter((item) => item.Status === "HIGH").length;

  return (
    <div className="app-shell">
      <header className="hero">
        <h1>🌍 CarbonEye AI</h1>
        <p>Automated detection of high-emission vehicles and industries.</p>
        <div className="actions">
          <button type="button" onClick={handleRunAnalysis} disabled={loading}>
            {loading ? "Running..." : "Run Emission Analysis"}
          </button>
          <a href={`${API_BASE}/download/vehicles`}>
            <button type="button" className="secondary">
              Download Vehicle Report
            </button>
          </a>
          <a href={`${API_BASE}/download/industries`}>
            <button type="button" className="secondary">
              Download Industry Report
            </button>
          </a>
        </div>
        <div className="banner">{message}</div>
      </header>

      <section className="grid">
        <div className="card">
          <h3>High Emission Vehicles</h3>
          <p>{highVehicleCount} flagged vehicles</p>
        </div>
        <div className="card">
          <h3>High Polluting Industries</h3>
          <p>{highIndustryCount} flagged industries</p>
        </div>
        <div className="card">
          <h3>Total Vehicles Scanned</h3>
          <p>{vehicles.length}</p>
        </div>
        <div className="card">
          <h3>Total Industries Scanned</h3>
          <p>{industries.length}</p>
        </div>
      </section>

      <h2 className="section-title">🚗 High Emission Vehicles</h2>
      <div className="card">
        <StatusTable
          rows={vehicles}
          columns={[
            { key: "vehicle_no", label: "Vehicle No" },
            { key: "Predicted_CO2", label: "Predicted CO₂" },
            { key: "Status", label: "Status" }
          ]}
        />
      </div>

      <h2 className="section-title">🏭 High Polluting Industries</h2>
      <div className="card">
        <StatusTable
          rows={industries}
          columns={[
            { key: "Industry_Name", label: "Industry" },
            { key: "Predicted_CO2", label: "Predicted CO₂" },
            { key: "Status", label: "Status" }
          ]}
        />
      </div>

      <h2 className="section-title">📊 Top Polluters Visualization</h2>
      <div className="chart-grid">
        <div className="card">
          <h3>Top 5 High Emission Vehicles</h3>
          <ResponsiveContainer width="100%" height={260}>
            <BarChart data={topVehicles}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="vehicle_no" />
              <YAxis tickFormatter={formatNumber} />
              <Tooltip />
              <Bar dataKey="Predicted_CO2" fill="#0f766e" />
            </BarChart>
          </ResponsiveContainer>
        </div>
        <div className="card">
          <h3>Top 5 High Polluting Industries</h3>
          <ResponsiveContainer width="100%" height={260}>
            <BarChart data={topIndustries}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="Industry_Name" />
              <YAxis tickFormatter={formatNumber} />
              <Tooltip />
              <Bar dataKey="Predicted_CO2" fill="#1d4ed8" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      <h2 className="section-title">📈 Emission Trend Analysis</h2>
      <div className="card">
        <ResponsiveContainer width="100%" height={280}>
          <LineChart data={trend}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="Index" />
            <YAxis tickFormatter={formatNumber} />
            <Tooltip />
            <Line type="monotone" dataKey="Predicted_CO2" stroke="#0f766e" />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
