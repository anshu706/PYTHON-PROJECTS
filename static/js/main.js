/* ═══════════════════════════════════════════════════════════════════════════
   PyLauncher — Enhanced Frontend Logic & Particle System
   ═══════════════════════════════════════════════════════════════════════════ */

(() => {
  "use strict";

  // ── DOM Elements ───────────────────────────────────────────────────────
  const grid         = document.getElementById("projects-grid");
  const searchIn     = document.getElementById("search-input");
  const navbar       = document.getElementById("navbar");
  const emptyState   = document.getElementById("empty-state");
  const heroStats    = document.getElementById("hero-stats");
  const sectionCount = document.getElementById("section-count");
  const statusText   = document.getElementById("status-text");
  
  // Decos
  const decoGames    = document.getElementById("deco-games");
  const decoUtils    = document.getElementById("deco-utils");
  const decoAdv      = document.getElementById("deco-adv");

  // View switches
  const viewGridBtn  = document.getElementById("view-grid");
  const viewListBtn  = document.getElementById("view-list");

  let allProjects    = [];
  let activeFilter   = "all";
  let currentLayout  = "grid"; // 'grid' or 'list'

  // ── Particle System Canvas ─────────────────────────────────────────────
  const canvas = document.getElementById("particle-canvas");
  const ctx = canvas.getContext("2d");

  let particles = [];
  const particleCount = 45;

  function resizeCanvas() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
  }

  class Particle {
    constructor() {
      this.reset();
    }
    reset() {
      this.x = Math.random() * canvas.width;
      this.y = Math.random() * canvas.height;
      this.size = Math.random() * 2 + 0.5;
      this.speedX = (Math.random() - 0.5) * 0.35;
      this.speedY = (Math.random() - 0.5) * 0.35;
      this.alpha = Math.random() * 0.5 + 0.1;
      this.hue = Math.random() > 0.5 ? 260 : 190; // violet or cyan
    }
    update() {
      this.x += this.speedX;
      this.y += this.speedY;

      if (this.x < 0 || this.x > canvas.width || this.y < 0 || this.y > canvas.height) {
        this.reset();
      }
    }
    draw() {
      ctx.fillStyle = `hsla(${this.hue}, 85%, 75%, ${this.alpha})`;
      ctx.shadowBlur = 8;
      ctx.shadowColor = `hsla(${this.hue}, 85%, 75%, ${this.alpha})`;
      ctx.beginPath();
      ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
      ctx.fill();
      ctx.shadowBlur = 0; // reset
    }
  }

  function initParticles() {
    resizeCanvas();
    particles = [];
    for (let i = 0; i < particleCount; i++) {
      particles.push(new Particle());
    }
  }

  function animateParticles() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    particles.forEach(p => {
      p.update();
      p.draw();
    });
    requestAnimationFrame(animateParticles);
  }

  window.addEventListener("resize", resizeCanvas);
  initParticles();
  animateParticles();

  // ── Fetch Projects ─────────────────────────────────────────────────────
  async function loadProjects() {
    try {
      const res = await fetch("/api/projects");
      allProjects = await res.json();
      
      statusText.textContent = `${allProjects.length} Online`;
      
      renderStats();
      renderGrid();
    } catch (err) {
      statusText.textContent = "Offline";
      grid.innerHTML = `
        <div style="color:var(--accent-rose);grid-column:1/-1;text-align:center;padding:60px;font-size:14px;font-family:var(--font-mono);border:1px solid rgba(244,63,94,0.15);background:rgba(244,63,94,0.03);border-radius:12px;">
          ✕ Failed to load projects. Is the backend server running?
        </div>
      `;
    }
  }

  // ── Render Stats ───────────────────────────────────────────────────────
  function renderStats() {
    const cats = { games: 0, utilities: 0, advanced: 0 };
    allProjects.forEach(p => {
      if (cats[p.category] !== undefined) {
        cats[p.category]++;
      }
    });

    // Update floating decorative card counts
    if (decoGames) decoGames.textContent = `${cats.games} app${cats.games !== 1 ? 's' : ''}`;
    if (decoUtils) decoUtils.textContent = `${cats.utilities} app${cats.utilities !== 1 ? 's' : ''}`;
    if (decoAdv)   decoAdv.textContent   = `${cats.advanced} app${cats.advanced !== 1 ? 's' : ''}`;

    // Update hero stats row
    if (heroStats) {
      heroStats.innerHTML = `
        <div class="stat-card">
          <span class="stat-number">${allProjects.length}</span>
          <span class="stat-label">Total Projects</span>
        </div>
        <div class="stat-card">
          <span class="stat-number">${cats.games}</span>
          <span class="stat-label">🎮 Games</span>
        </div>
        <div class="stat-card">
          <span class="stat-number">${cats.utilities}</span>
          <span class="stat-label">🛠️ Utilities</span>
        </div>
        <div class="stat-card">
          <span class="stat-number">${cats.advanced}</span>
          <span class="stat-label">🚀 Advanced</span>
        </div>
      `;
    }
  }

  // ── Render Grid ────────────────────────────────────────────────────────
  function renderGrid() {
    const query = searchIn.value.trim().toLowerCase();
    const filtered = allProjects.filter(p => {
      const matchCat = activeFilter === "all" || p.category === activeFilter;
      const matchSearch = !query
        || p.title.toLowerCase().includes(query)
        || p.desc.toLowerCase().includes(query)
        || p.tags.some(t => t.toLowerCase().includes(query));
      return matchCat && matchSearch;
    });

    if (sectionCount) {
      sectionCount.textContent = `${filtered.length} project${filtered.length !== 1 ? "s" : ""}`;
    }

    if (filtered.length === 0) {
      grid.innerHTML = "";
      emptyState.style.display = "flex";
      return;
    }

    emptyState.style.display = "none";

    // Build project elements
    grid.className = `projects-grid ${currentLayout === "list" ? "list-mode" : ""}`;
    grid.innerHTML = filtered.map((p, i) => {
      const categoryColor = p.category === 'games' ? '#f43f5e' : (p.category === 'utilities' ? '#38bdf8' : '#a78bfa');
      const tagHTML = p.tags.map(t => `<span class="tag tag-${t.toLowerCase()}">${t}</span>`).join("");
      
      return `
        <article class="card" style="animation: slideInToast 0.4s var(--ease-out-expo) both; animation-delay: ${i * 0.03}s" data-path="${p.path}">
          <div class="card-top">
            <div class="card-meta">
              <span class="card-category">
                <span class="category-dot" style="background:${categoryColor}; box-shadow: 0 0 6px ${categoryColor}"></span>
                ${p.catLabel}
              </span>
              <div class="card-icon-wrap">${p.icon}</div>
            </div>
            <div class="card-info">
              <h3 class="card-title">${p.title}</h3>
              <p class="card-desc">${p.desc}</p>
            </div>
          </div>
          <div class="card-bottom">
            <div class="card-tags">${tagHTML}</div>
            <button class="btn-launch" onclick="window.__launch('${p.path}', '${p.type}', '${p.web_url}', this)" id="launch-${p.filename}">
              <span>Launch</span>
              <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <line x1="5" y1="12" x2="11" y2="6"></line>
                <polyline points="11 11 11 6 6 6"></polyline>
              </svg>
            </button>
          </div>
        </article>
      `;
    }).join("");
  }

  // ── Launch Project ─────────────────────────────────────────────────────
  window.__launch = async function(path, type, webUrl, btn) {
    if (type === 'web') {
      window.open(webUrl, '_blank');
      showToast("Web App Opened", `Successfully opened web app in new tab.`, "success");
      return;
    }

    btn.classList.add("launching");
    const originalContent = btn.innerHTML;
    btn.innerHTML = `
      <span>Launching</span>
      <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M8 1.5a6.5 6.5 0 1 0 6.5 6.5" stroke-linecap="round"/>
      </svg>
    `;

    try {
      const res = await fetch("/api/launch", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ path }),
      });
      const data = await res.json();

      if (data.status === "ok") {
        showToast("Process Started", `Successfully launched native application.`, "success");
      } else {
        showToast("Launch Failed", data.message || "Could not launch app.", "error");
      }
    } catch (err) {
      showToast("Network Error", "Unable to communicate with PyLauncher backend.", "error");
    }

    setTimeout(() => {
      btn.classList.remove("launching");
      btn.innerHTML = originalContent;
    }, 1500);
  };

  // ── Dynamic Toast Stacking System ──────────────────────────────────────
  const toastStack = document.getElementById("toast-stack");

  function showToast(title, message, type = "success") {
    if (!toastStack) return;

    const toast = document.createElement("div");
    toast.className = `toast ${type}`;
    
    const icon = type === "success" ? "✓" : "✕";
    
    toast.innerHTML = `
      <span class="toast-icon">${icon}</span>
      <div class="toast-content">
        <div class="toast-title">${title}</div>
        <div class="toast-msg">${message}</div>
      </div>
      <button class="toast-close" aria-label="Close message">×</button>
    `;

    toastStack.appendChild(toast);

    const closeBtn = toast.querySelector(".toast-close");
    closeBtn.addEventListener("click", () => removeToast(toast));

    // Auto-remove
    setTimeout(() => {
      removeToast(toast);
    }, 4000);
  }

  function removeToast(toast) {
    toast.classList.add("removing");
    toast.addEventListener("transitionend", () => {
      toast.remove();
    });
  }

  // ── Filters & Interactions ─────────────────────────────────────────────
  document.querySelectorAll(".filter-chip").forEach(chip => {
    chip.addEventListener("click", () => {
      document.querySelectorAll(".filter-chip").forEach(c => c.classList.remove("active"));
      chip.classList.add("active");
      activeFilter = chip.dataset.filter;
      renderGrid();
    });
  });

  window.__resetFilters = function() {
    activeFilter = "all";
    document.querySelectorAll(".filter-chip").forEach(c => {
      c.classList.toggle("active", c.dataset.filter === "all");
    });
    renderGrid();
  };

  searchIn.addEventListener("input", renderGrid);

  // ── Keyboard shortcuts ─────────────────────────────────────────────────
  window.addEventListener("keydown", (e) => {
    // Cmd/Ctrl + K to focus search
    if ((e.metaKey || e.ctrlKey) && e.key === "k") {
      e.preventDefault();
      searchIn.focus();
    }
  });

  // ── Sticky Navbar Visuals ──────────────────────────────────────────────
  window.addEventListener("scroll", () => {
    navbar.classList.toggle("scrolled", window.scrollY > 20);
  }, { passive: true });

  // ── Layout Switcher ────────────────────────────────────────────────────
  if (viewGridBtn && viewListBtn) {
    viewGridBtn.addEventListener("click", () => {
      currentLayout = "grid";
      viewGridBtn.classList.add("active");
      viewListBtn.classList.remove("active");
      renderGrid();
    });

    viewListBtn.addEventListener("click", () => {
      currentLayout = "list";
      viewListBtn.classList.add("active");
      viewGridBtn.classList.remove("active");
      renderGrid();
    });
  }

  // ── Boot ───────────────────────────────────────────────────────────────
  loadProjects();
})();
