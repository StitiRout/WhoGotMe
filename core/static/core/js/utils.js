function getRiskColor(score) {
  if (score >= 75) return "#ff3864";
  if (score >= 50) return "#f59e0b";
  if (score >= 25) return "#00f0ff";
  return "#00ff88";
}

function getRiskLabel(score) {
  if (score >= 75) return "CRITICAL";
  if (score >= 50) return "HIGH";
  if (score >= 25) return "MEDIUM";
  return "LOW";
}

function buildRiskBar(score, animated) {
  const color = getRiskColor(score);
  const label = getRiskLabel(score);
  const width = animated ? "0%" : score + "%";

  const html = `
    <div class="risk-bar">
      <div class="risk-bar-header">
        <span class="risk-bar-label">Risk Score</span>
        <span class="risk-bar-value" style="color:${color}">${score}% — ${label}</span>
      </div>
      <div class="risk-bar-track">
        <div class="risk-bar-fill" style="width:${width}"></div>
      </div>
      <div class="risk-bar-scale">
        <span>LOW</span><span>MEDIUM</span><span>HIGH</span><span>CRITICAL</span>
      </div>
    </div>`;

  return { html, color, score };
}

function animateRiskBar(container) {
  const fill = container.querySelector(".risk-bar-fill");
  const valueEl = container.querySelector(".risk-bar-value");
  if (!fill || !valueEl) return;

  const target = parseInt(valueEl.textContent, 10) || 0;
  let current = 0;

  function step() {
    current += 1.5;
    if (current >= target) {
      fill.style.width = target + "%";
      return;
    }
    fill.style.width = Math.round(current) + "%";
    requestAnimationFrame(step);
  }

  requestAnimationFrame(step);
}

function getCsrfToken() {
  return window.WGM_CSRF || "";
}

async function postJSON(url, data) {
  const response = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCsrfToken(),
    },
    body: JSON.stringify(data),
  });
  const json = await response.json();
  if (!response.ok) {
    throw new Error(json.error || "Request failed");
  }
  return json;
}
