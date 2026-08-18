import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:8000/api/v1";

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// ===============================
// Predictions
// ===============================

export const createPrediction = async (shipmentData) => {
  const response = await api.post("/predictions/", shipmentData);
  return response.data;
};

export const getPredictions = async (skip = 0, limit = 20) => {
  const response = await api.get("/predictions/", {
    params: { skip, limit },
  });
  return response.data;
};

export const getPrediction = async (predictionId) => {
  const response = await api.get(`/predictions/${predictionId}`);
  return response.data;
};

export const getShipmentPrediction = async (shipmentId) => {
  const response = await api.get(`/predictions/shipment/${shipmentId}`);
  return response.data;
};

// ===============================
// Optimization
// ===============================

export const simulateOptimization = async (shipmentData) => {
  const response = await api.post("/optimization/simulate", shipmentData);
  return response.data;
};

export const getTransportModes = async () => {
  const response = await api.get("/optimization/modes");
  return response.data;
};

// ===============================
// Decisions
// ===============================

export const executeDecision = async (decisionData) => {
  const response = await api.post("/decisions/execute", decisionData);
  return response.data;
};

export const evaluateDecision = async (decisionId, evaluationData) => {
  const response = await api.post(
    `/decisions/${decisionId}/evaluate`,
    evaluationData
  );
  return response.data;
};

export const getDecisions = async (skip = 0, limit = 20) => {
  const response = await api.get("/decisions", {
    params: { skip, limit },
  });
  return response.data;
};

export const getDecisionAnalytics = async () => {
  const response = await api.get("/decisions/analytics");
  return response.data;
};

// ===============================
// Analytics
// ===============================

export const getAnalyticsSummary = async () => {
  const response = await api.get("/analytics/summary");
  return response.data;
};

export const getAnalyticsBreakdown = async () => {
  const response = await api.get("/analytics/breakdown");
  return response.data;
};

export const batchPredict = async (shipments) => {
  const response = await api.post("/predictions/batch", {
    shipments,
  });
  return response.data;
};

// ===============================
// Reports
// ===============================

export const uploadCSV = async (file) => {
  const formData = new FormData();
  formData.append("file", file);

  const response = await api.post("/reports/upload-csv", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });

  return response.data;
};

export const exportCSV = async () => {
  const response = await api.get("/reports/export-csv", {
    responseType: "blob",
  });

  return response.data;
};

export default api;