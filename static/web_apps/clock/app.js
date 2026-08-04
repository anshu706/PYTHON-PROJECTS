/* ═══════════════════════════════════════════════════════════════════════════
   SpaceClock - JavaScript controller
   ═══════════════════════════════════════════════════════════════════════════ */

(() => {
  "use strict";

  // ── Clock display logic ────────────────────────────────────────────────
  function updateClock() {
    const now = new Date();
    
    let hours = now.getHours();
    let minutes = now.getMinutes();
    let seconds = now.getSeconds();
    let ampm = hours >= 12 ? 'PM' : 'AM';
    
    hours = hours % 12;
    hours = hours ? hours : 12; // 0 is 12
    
    hours = hours < 10 ? '0' + hours : hours;
    minutes = minutes < 10 ? '0' + minutes : minutes;
    seconds = seconds < 10 ? '0' + seconds : seconds;
    
    document.getElementById('time').textContent = `${hours}:${minutes}:${seconds}`;
    document.getElementById('ampm').textContent = ampm;
    
    const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
    document.getElementById('date').textContent = now.toLocaleDateString(undefined, options);
  }

  // Set GMT/Timezone indicator
  function updateTimezone() {
    const tzName = Intl.DateTimeFormat().resolvedOptions().timeZone;
    const offsetMin = new Date().getTimezoneOffset();
    const offsetHour = Math.abs(offsetMin / 60);
    const offsetSign = offsetMin <= 0 ? "+" : "-";
    const formattedOffset = `UTC ${offsetSign}${String(Math.floor(offsetHour)).padStart(2, '0')}:${String(Math.abs(offsetMin % 60)).padStart(2, '0')}`;
    
    document.getElementById("timezone").textContent = `${tzName} (${formattedOffset})`;
  }

  // ── Tabs switching ──────────────────────────────────────────────────────
  document.querySelectorAll(".tab-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      document.querySelectorAll(".tab-btn").forEach(b => b.classList.remove("active"));
      document.querySelectorAll(".tab-pane").forEach(p => p.classList.remove("active"));
      
      btn.classList.add("active");
      document.getElementById(`pane-${btn.dataset.tab}`).classList.add("active");
    });
  });

  // ── Themes switching ────────────────────────────────────────────────────
  document.querySelectorAll(".theme-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      document.querySelectorAll(".theme-btn").forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      
      // Remove previous body themes
      document.body.className = "";
      if (btn.dataset.theme !== "cyan") {
        document.body.classList.add(`theme-${btn.dataset.theme}`);
      }
    });
  });

  // ── Stopwatch Logic ─────────────────────────────────────────────────────
  let swTimer = null;
  let swElapsed = 0; // milliseconds
  let swStartTime = 0;
  let swRunning = false;
  let laps = [];

  const swDisplay = document.getElementById("stopwatch-time");
  const swStartBtn = document.getElementById("sw-start");
  const swLapBtn = document.getElementById("sw-lap");
  const swResetBtn = document.getElementById("sw-reset");
  const lapsList = document.getElementById("laps-list");

  function formatTime(ms) {
    let minutes = Math.floor(ms / 60000);
    let seconds = Math.floor((ms % 60000) / 1000);
    let centiseconds = Math.floor((ms % 1000) / 10);
    
    return `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}.${String(centiseconds).padStart(2, '0')}`;
  }

  function swUpdate() {
    const now = Date.now();
    const currentElapsed = swElapsed + (now - swStartTime);
    swDisplay.textContent = formatTime(currentElapsed);
  }

  swStartBtn.addEventListener("click", () => {
    if (swRunning) {
      // Pause
      swRunning = false;
      swElapsed += Date.now() - swStartTime;
      clearInterval(swTimer);
      swStartBtn.textContent = "Resume";
      swStartBtn.classList.remove("secondary");
      swLapBtn.disabled = true;
    } else {
      // Start
      swRunning = true;
      swStartTime = Date.now();
      swTimer = setInterval(swUpdate, 10);
      swStartBtn.textContent = "Pause";
      swStartBtn.classList.add("secondary");
      swLapBtn.disabled = false;
    }
  });

  swLapBtn.addEventListener("click", () => {
    if (!swRunning) return;
    const now = Date.now();
    const currentElapsed = swElapsed + (now - swStartTime);
    
    laps.unshift(currentElapsed);
    
    const lapRow = document.createElement("div");
    lapRow.className = "lap-row";
    lapRow.innerHTML = `
      <span>Lap ${laps.length}</span>
      <span>${formatTime(currentElapsed)}</span>
    `;
    lapsList.insertBefore(lapRow, lapsList.firstChild);
  });

  swResetBtn.addEventListener("click", () => {
    swRunning = false;
    clearInterval(swTimer);
    swElapsed = 0;
    laps = [];
    swDisplay.textContent = "00:00.00";
    swStartBtn.textContent = "Start";
    swStartBtn.classList.remove("secondary");
    swLapBtn.disabled = true;
    lapsList.innerHTML = "";
  });

  // Simulated dynamic latency ping
  setInterval(() => {
    const ping = Math.floor(Math.random() * 8) + 8;
    document.getElementById("simulated-ping").textContent = `PING: ${ping}ms`;
  }, 3000);

  // Boot
  updateClock();
  updateTimezone();
  setInterval(updateClock, 1000);
})();
