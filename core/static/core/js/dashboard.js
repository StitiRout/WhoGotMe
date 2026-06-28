(function () {
  const dataEl = document.getElementById("wgm-data");
  const data = dataEl ? JSON.parse(dataEl.textContent) : null;
  if (!data) return;

  const chartDefaults = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: { legend: { display: false } },
  };

  const mutedTick = { color: "#5a7a9a", font: { family: "JetBrains Mono", size: 10 } };

  // Timeline area chart
  const timelineCtx = document.getElementById("timeline-chart");
  if (timelineCtx) {
    new Chart(timelineCtx, {
      type: "line",
      data: {
        labels: data.timeline.map((d) => d.month),
        datasets: [{
          label: "breaches",
          data: data.timeline.map((d) => d.breach_count),
          borderColor: "#00f0ff",
          backgroundColor: "rgba(0,240,255,0.15)",
          fill: true,
          tension: 0.4,
          pointRadius: 0,
        }],
      },
      options: {
        ...chartDefaults,
        scales: {
          x: { ticks: mutedTick, grid: { color: "rgba(255,255,255,0.04)" } },
          y: { ticks: mutedTick, grid: { color: "rgba(255,255,255,0.04)" } },
        },
      },
    });
  }

  // Risk donut chart
  const riskCtx = document.getElementById("risk-chart");
  const legendEl = document.getElementById("risk-legend");
  if (riskCtx) {
    new Chart(riskCtx, {
      type: "doughnut",
      data: {
        labels: data.riskDist.map((d) => d.name),
        datasets: [{
          data: data.riskDist.map((d) => d.value),
          backgroundColor: data.riskDist.map((d) => d.color),
          borderWidth: 0,
        }],
      },
      options: {
        ...chartDefaults,
        cutout: "55%",
      },
    });

    if (legendEl) {
      legendEl.innerHTML = data.riskDist
        .map(
          (d) => `
          <div class="risk-legend-item">
            <span class="dot" style="background:${d.color}"></span>
            <span>${d.name}</span>
            <span class="pct" style="color:${d.color}">${d.value}%</span>
          </div>`
        )
        .join("");
    }
  }

  // Sources bar chart
  const sourcesCtx = document.getElementById("sources-chart");
  if (sourcesCtx) {
    new Chart(sourcesCtx, {
      type: "bar",
      data: {
        labels: data.sources.map((d) => d.source),
        datasets: [{
          label: "count",
          data: data.sources.map((d) => d.count),
          backgroundColor: "rgba(0,240,255,0.8)",
          borderRadius: 4,
        }],
      },
      options: {
        ...chartDefaults,
        indexAxis: "y",
        scales: {
          x: { ticks: mutedTick, grid: { color: "rgba(255,255,255,0.04)" } },
          y: { ticks: mutedTick, grid: { display: false } },
        },
      },
    });
  }

  // Attack intelligence search
  const attackInput = document.getElementById("attack-input");
  const searchBtn = document.getElementById("attack-search-btn");
  const loadingEl = document.getElementById("attack-loading");
  const resultEl = document.getElementById("attack-result");
  const suggestionsEl = document.getElementById("attack-suggestions");

  async function searchAttack(query) {
    if (!query.trim()) return;

    loadingEl.classList.remove("hidden");
    resultEl.classList.add("hidden");
    suggestionsEl.classList.add("hidden");

    try {
      const res = await fetch(
        `${data.apiAttack}?q=${encodeURIComponent(query.trim())}`
      );
      const json = await res.json();

      loadingEl.classList.add("hidden");
      resultEl.classList.remove("hidden");

      if (json.found && json.data) {
        resultEl.className = "attack-result found";
        resultEl.innerHTML = `
          <h4>${json.query}</h4>
          <div class="attack-field">
            <div class="attack-field-label">Summary</div>
            <p>${json.data.summary}</p>
          </div>
          <div class="attack-field">
            <div class="attack-field-label">Vector</div>
            <p>${json.data.vector}</p>
          </div>
          <div class="attack-field">
            <div class="attack-field-label">Mitigation</div>
            <p>${json.data.mitigation}</p>
          </div>
          ${json.data.cve ? `<div class="attack-field-label">CVE: ${json.data.cve}</div>` : ""}`;
      } else {
        resultEl.className = "attack-result not-found";
        resultEl.textContent = `No data for "${json.query}" — try: SQL Injection, Phishing, Ransomware, XSS, DDoS`;
        suggestionsEl.classList.remove("hidden");
      }
    } catch {
      loadingEl.classList.add("hidden");
      resultEl.classList.remove("hidden");
      resultEl.className = "attack-result not-found";
      resultEl.textContent = "Failed to fetch attack info.";
    }
  }

  searchBtn.addEventListener("click", () => searchAttack(attackInput.value));
  attackInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter") searchAttack(attackInput.value);
  });

  suggestionsEl.querySelectorAll("button").forEach((btn) => {
    btn.addEventListener("click", () => {
      attackInput.value = btn.dataset.query;
      searchAttack(btn.dataset.query);
    });
  });
})();
