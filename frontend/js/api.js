const API_BASE = "http://localhost:8000/api";

function getToken() {
  return localStorage.getItem("token");
}

async function apiRequest(endpoint, method = "GET", data = null, auth = true) {
  const headers = {
    "Content-Type": "application/json"
  };
  if (auth && getToken()) {
    headers["Authorization"] = `Bearer ${getToken()}`;
  }

  const config = {
    method,
    headers
  };
  if (data) {
    config.body = JSON.stringify(data);
  }

  const res = await fetch(`${API_BASE}${endpoint}`, config);
  return res.json();
}
