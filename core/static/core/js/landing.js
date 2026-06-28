(function () {
  const emailInput = document.getElementById("email-input");
  const checkBtn = document.getElementById("check-btn");
  const errorMsg = document.getElementById("error-msg");

  const states = {
    idle: document.getElementById("state-idle"),
    loading: document.getElementById("state-loading"),
    clean: document.getElementById("state-clean"),
    results: document.getElementById("state-results"),
  };

  function showState(name) {
    Object.entries(states).forEach(([key, el]) => {
      if (!el) return;
      el.classList.toggle("hidden", key !== name);
    });
  }

  function resetForm() {
    emailInput.value = "";
    emailInput.classList.remove("error");
    errorMsg.classList.add("hidden");
    showState("idle");
  }

  function renderBreachCard(breach) {
    return `
      <div class="glass-card breach-card">
        <div class="breach-card-top">
          <div class="breach-name-row">
            <span class="breach-name">${breach.name}</span>
            <span class="severity-badge severity-${breach.severity}">${breach.severity}</span>
          </div>
          <span class="breach-date">${breach.date}</span>
        </div>
        <p class="breach-desc">${breach.description}</p>
        <div class="data-tags">
          ${breach.dataTypes.map((dt) => `<span class="data-tag">${dt}</span>`).join("")}
        </div>
      </div>`;
  }

  function showResults(data) {
    document.getElementById("result-email").textContent = data.maskedEmail;
    document.getElementById("breach-count").textContent =
      data.breachCount + " breach" + (data.breachCount !== 1 ? "es" : "");

    const riskContainer = document.getElementById("risk-bar-container");
    const risk = buildRiskBar(data.riskScore, true);
    riskContainer.innerHTML = risk.html;

    document.getElementById("breach-list").innerHTML = data.breaches
      .map(renderBreachCard)
      .join("");

    showState("results");
    animateRiskBar(riskContainer);
  }

  function showClean(data) {
    document.getElementById("clean-email").textContent = data.maskedEmail;
    showState("clean");
  }

  async function handleCheck() {
    const email = emailInput.value.trim();
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (!emailRegex.test(email)) {
      emailInput.classList.add("error");
      errorMsg.classList.remove("hidden");
      return;
    }

    emailInput.classList.remove("error");
    errorMsg.classList.add("hidden");
    showState("loading");

    try {
      const data = await postJSON(window.WGM_API_CHECK, { email });
      if (data.isClean) {
        showClean(data);
      } else {
        showResults(data);
      }
    } catch (err) {
      showState("idle");
      errorMsg.textContent = err.message;
      errorMsg.classList.remove("hidden");
    }
  }

  checkBtn.addEventListener("click", handleCheck);
  emailInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter") handleCheck();
  });

  ["reset-clean-btn", "reset-results-btn", "reset-another-btn"].forEach((id) => {
    const btn = document.getElementById(id);
    if (btn) btn.addEventListener("click", resetForm);
  });

  // Particle background
  const canvas = document.getElementById("particle-canvas");
  if (!canvas) return;

  const ctx = canvas.getContext("2d");
  canvas.width = canvas.offsetWidth;
  canvas.height = canvas.offsetHeight;

  const particles = [];
  for (let i = 0; i < 60; i++) {
    particles.push({
      x: Math.random() * canvas.width,
      y: Math.random() * canvas.height,
      vx: (Math.random() - 0.5) * 0.4,
      vy: (Math.random() - 0.5) * 0.4,
      size: Math.random() * 1.5 + 0.5,
      alpha: Math.random() * 0.5 + 0.1,
    });
  }

  function drawParticles() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    particles.forEach((p) => {
      p.x += p.vx;
      p.y += p.vy;
      if (p.x < 0 || p.x > canvas.width) p.vx *= -1;
      if (p.y < 0 || p.y > canvas.height) p.vy *= -1;
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(0,240,255,${p.alpha})`;
      ctx.fill();
    });
    for (let i = 0; i < particles.length; i++) {
      for (let j = i + 1; j < particles.length; j++) {
        const dx = particles[i].x - particles[j].x;
        const dy = particles[i].y - particles[j].y;
        const dist = Math.sqrt(dx * dx + dy * dy);
        if (dist < 100) {
          ctx.beginPath();
          ctx.moveTo(particles[i].x, particles[i].y);
          ctx.lineTo(particles[j].x, particles[j].y);
          ctx.strokeStyle = `rgba(0,240,255,${0.05 * (1 - dist / 100)})`;
          ctx.lineWidth = 0.5;
          ctx.stroke();
        }
      }
    }
    requestAnimationFrame(drawParticles);
  }

  drawParticles();
  window.addEventListener("resize", () => {
    canvas.width = canvas.offsetWidth;
    canvas.height = canvas.offsetHeight;
  });
})();
