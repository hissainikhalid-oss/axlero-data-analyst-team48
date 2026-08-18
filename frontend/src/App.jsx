import { useState } from "react";
import "./App.css";

function App() {
  const [budget, setBudget] = useState(20000);
  const [maxDelay, setMaxDelay] = useState(5);

  // STEP 1 — Shipment states
  const [origin, setOrigin] = useState("Mumbai");
  const [destination, setDestination] = useState("Delhi");
  const [distance, setDistance] = useState(1400);
  const [weather, setWeather] = useState("Storm");
  const [traffic, setTraffic] = useState("High");
  const [vehicleType, setVehicleType] = useState("Container");
  const [urgencyLevel, setUrgencyLevel] = useState("High");

  const [optimizationResult, setOptimizationResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // STEP 4 — Run backend optimization
  const runOptimization = async () => {
    setLoading(true);
    setError("");

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/api/v1/optimization/simulate",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            origin: origin,
            destination: destination,
            distance: Number(distance),
            weather: weather,
            traffic: traffic,
            vehicle_type: vehicleType,
            urgency_level: urgencyLevel,
          }),
        }
      );

      if (!response.ok) {
        throw new Error(`HTTP error: ${response.status}`);
      }

      const data = await response.json();

      console.log("Optimization result:", data);

      setOptimizationResult(data);
    } catch (err) {
      console.error("Optimization error:", err);
      setError("Unable to connect to backend.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">

      {/* Header */}
      <header className="header">
        <div>
          <div className="brand">SUPPLY PRESCRIPT</div>
          <div className="subtitle">
            Decision Intelligence Console
          </div>
        </div>

        <div className="status">
          <span className="status-dot"></span>
          SYSTEM ONLINE
        </div>
      </header>

      {/* Main */}
      <main className="container">

        {/* Hero */}
        <section className="hero">
          <div>
            <p className="eyebrow">
              OPTIMIZATION CONTROL TOWER
            </p>

            <h1>Supply Chain Decision Console</h1>

            <p className="hero-text">
              Adjust your business constraints and evaluate the best
              available recovery strategy.
            </p>
          </div>

          <div className="prediction-box">
            <span>Predicted Delay</span>
            <strong>14 DAYS</strong>
            <small>ML prediction</small>
          </div>
        </section>

        {/* STEP 6 — Shipment Inputs */}
        <section className="shipment-inputs">

          <div className="control-card">
            <div className="control-heading">
              <span>ORIGIN</span>
            </div>

            <input
              type="text"
              value={origin}
              onChange={(e) => setOrigin(e.target.value)}
            />
          </div>

          <div className="control-card">
            <div className="control-heading">
              <span>DESTINATION</span>
            </div>

            <input
              type="text"
              value={destination}
              onChange={(e) => setDestination(e.target.value)}
            />
          </div>

          <div className="control-card">
            <div className="control-heading">
              <span>DISTANCE (KM)</span>
            </div>

            <input
              type="number"
              value={distance}
              onChange={(e) => setDistance(e.target.value)}
            />
          </div>

          <div className="control-card">
            <div className="control-heading">
              <span>WEATHER</span>
            </div>

            <select
              value={weather}
              onChange={(e) => setWeather(e.target.value)}
            >
              <option value="Clear">Clear</option>
              <option value="Rain">Rain</option>
              <option value="Storm">Storm</option>
            </select>
          </div>

          <div className="control-card">
            <div className="control-heading">
              <span>TRAFFIC</span>
            </div>

            <select
              value={traffic}
              onChange={(e) => setTraffic(e.target.value)}
            >
              <option value="Low">Low</option>
              <option value="Medium">Medium</option>
              <option value="High">High</option>
            </select>
          </div>

          <div className="control-card">
            <div className="control-heading">
              <span>VEHICLE TYPE</span>
            </div>

            <select
              value={vehicleType}
              onChange={(e) => setVehicleType(e.target.value)}
            >
              <option value="Container">Container</option>
              <option value="Truck">Truck</option>
              <option value="Express Truck">
                Express Truck
              </option>
            </select>
          </div>

          <div className="control-card">
            <div className="control-heading">
              <span>URGENCY</span>
            </div>

            <select
              value={urgencyLevel}
              onChange={(e) => setUrgencyLevel(e.target.value)}
            >
              <option value="Low">Low</option>
              <option value="Medium">Medium</option>
              <option value="High">High</option>
            </select>
          </div>

        </section>

        {/* STEP 5 — Existing Controls */}
        <section className="controls">

          {/* Budget */}
          <div className="control-card">

            <div className="control-heading">
              <span>AVAILABLE BUDGET</span>

              <strong>
                ${budget.toLocaleString()}
              </strong>
            </div>

            <input
              type="range"
              min="0"
              max="30000"
              step="1000"
              value={budget}
              onChange={(e) =>
                setBudget(Number(e.target.value))
              }
            />

            <div className="range-labels">
              <span>$0</span>
              <span>$30,000</span>
            </div>

          </div>

          {/* Maximum Delay */}
          <div className="control-card">

            <div className="control-heading">
              <span>MAXIMUM ACCEPTABLE DELAY</span>

              <strong>
                {maxDelay} DAYS
              </strong>
            </div>

            <input
              type="range"
              min="0"
              max="14"
              value={maxDelay}
              onChange={(e) =>
                setMaxDelay(Number(e.target.value))
              }
            />

            <div className="range-labels">
              <span>0 days</span>
              <span>14 days</span>
            </div>

          </div>

        </section>

        {/* STEP 7 — Optimization Button */}
        <button
          className="optimize-button"
          onClick={runOptimization}
          disabled={loading}
        >
          {loading
            ? "OPTIMIZING..."
            : "RUN OPTIMIZATION"}
        </button>

        {error && (
          <p className="error-message">
            {error}
          </p>
        )}

        {/* STEP 8/9 — Decision Compass */}
        <section className="decision-section">

          <div className="section-title">

            <div>
              <p className="eyebrow">
                LIVE OPTIMIZATION
              </p>

              <h2>Decision Compass</h2>
            </div>

            <div className="legend">
              <span className="legend-cost">
                COST →
              </span>

              <span>
                DELAY ↑
              </span>
            </div>

          </div>

          <div className="compass">

            <div className="axis-y">
              DELAY
            </div>

            <div className="quadrant q1">
              <span>HIGH COST</span>
              <span>HIGH DELAY</span>
            </div>

            <div className="quadrant q2">
              <span>LOW COST</span>
              <span>HIGH DELAY</span>
            </div>

            <div className="quadrant q3">
              <span>LOW COST</span>
              <span>LOW DELAY</span>
            </div>

            <div className="quadrant q4">
              <span>HIGH COST</span>
              <span>LOW DELAY</span>
            </div>

          </div>

          {/* STEP 9 */}
          <div className="point-labels">

            {optimizationResult?.all_options?.map(
              (option, index) => (

                <div
                  key={option.transport_mode}
                  className="point-label"
                >

                  <span
                    className={`mini-point point-${index + 1}`}
                  ></span>

                  <div>

                    <strong>
                      {option.transport_mode}
                    </strong>

                    <small>
                      ₹
                      {Number(
                        option.estimated_cost
                      ).toLocaleString()}
                      {" · "}
                      {option.estimated_hours}
                      {" hours"}
                    </small>

                  </div>

                </div>
              )
            )}

          </div>

        </section>

        {/* STEP 10/11 — Recommendation */}
        <section className="recommendation">

          <div className="recommendation-header">

            <div>
              <p className="eyebrow">
                OPTIMIZER OUTPUT
              </p>

              <h2>
                Recommended Decision
              </h2>
            </div>

            {optimizationResult ? (
              <span className="recommended-badge">
                RECOMMENDED
              </span>
            ) : (
              <span className="warning-badge">
                RUN OPTIMIZATION
              </span>
            )}

          </div>

          {/* STEP 11 */}
          {optimizationResult && (
            <div className="recommendation-result">

              <h3>
                {optimizationResult.optimal_mode}
              </h3>

              <p>
                {optimizationResult.recommendation_summary}
              </p>

              <div className="result-grid">

                <div>
                  <span>ORIGINAL MODE</span>

                  <strong>
                    {optimizationResult.original_mode}
                  </strong>
                </div>

                <div>
                  <span>OPTIMAL MODE</span>

                  <strong>
                    {optimizationResult.optimal_mode}
                  </strong>
                </div>

                <div>
                  <span>TIME SAVED</span>

                  <strong>
                    {optimizationResult.time_saved_hours}
                    {" hours"}
                  </strong>
                </div>

                <div>
                  <span>COST IMPACT</span>

                  <strong>
                    ₹
                    {Number(
                      optimizationResult.cost_impact
                    ).toLocaleString()}
                  </strong>
                </div>

                <div>
                  <span>RISK REDUCTION</span>

                  <strong>
                    {
                      optimizationResult
                        .risk_reduction_percentage
                    }
                    %
                  </strong>
                </div>

              </div>

            </div>
          )}

        </section>

        {/* Backend options */}
        {optimizationResult?.all_options?.length > 0 && (
          <section className="options-section">

            <div className="section-title">
              <div>
                <p className="eyebrow">
                  AVAILABLE STRATEGIES
                </p>

                <h2>
                  Optimization Options
                </h2>
              </div>
            </div>

            <div className="options-grid">

              {optimizationResult.all_options.map(
                (option) => {

                  const isRecommended =
                    option.transport_mode ===
                    optimizationResult.optimal_mode;

                  return (
                    <div
                      className={`option-card ${
                        isRecommended
                          ? "best-card"
                          : ""
                      }`}
                      key={option.transport_mode}
                    >

                      <div className="option-top">

                        <span className="option-number">
                          {option.transport_mode}
                        </span>

                        {isRecommended && (
                          <span className="best">
                            BEST
                          </span>
                        )}

                      </div>

                      <h3>
                        {option.transport_mode}
                      </h3>

                      <p>
                        {isRecommended
                          ? "Recommended optimization option."
                          : "Available transportation option."}
                      </p>

                      <div className="option-metrics">

                        <div>
                          <span>COST</span>

                          <strong>
                            ₹
                            {Number(
                              option.estimated_cost
                            ).toLocaleString()}
                          </strong>
                        </div>

                        <div>
                          <span>TIME</span>

                          <strong>
                            {option.estimated_hours}
                            {" HOURS"}
                          </strong>
                        </div>

                      </div>

                      <div
                        className={
                          isRecommended
                            ? "feasible"
                            : "not-feasible"
                        }
                      >
                        {isRecommended
                          ? "✓ RECOMMENDED"
                          : "AVAILABLE OPTION"}
                      </div>

                    </div>
                  );
                }
              )}

            </div>

          </section>
        )}

      </main>
    </div>
  );
}

export default App;