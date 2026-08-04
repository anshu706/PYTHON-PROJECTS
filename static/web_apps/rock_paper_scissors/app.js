/* ═══════════════════════════════════════════════════════════════════════════
   RPS Arena — JavaScript Logic
   ═══════════════════════════════════════════════════════════════════════════ */

(() => {
  "use strict";

  const choices       = document.querySelectorAll('.choice-btn');
  const statusText    = document.getElementById('status');
  const playerScoreEl = document.getElementById('player-score');
  const compScoreEl   = document.getElementById('computer-score');
  const streakValEl   = document.getElementById('streak-val');
  const resetBtn      = document.getElementById('reset-btn');

  // Match slot selectors
  const pGestureEl    = document.getElementById('player-gesture');
  const cGestureEl    = document.getElementById('computer-gesture');

  let playerScore = 0;
  let computerScore = 0;
  let winStreak = 0;

  const options = ['rock', 'paper', 'scissors'];
  const emojis = { 'rock': '✊', 'paper': '✋', 'scissors': '✌️' };

  choices.forEach(btn => btn.addEventListener('click', playGame));
  resetBtn.addEventListener('click', resetGame);

  async function playGame(e) {
    // Disable buttons during evaluation
    setButtonsDisabled(true);

    const playerChoice = e.target.getAttribute('data-choice') || e.target.closest('button').getAttribute('data-choice');
    pGestureEl.textContent = emojis[playerChoice];
    pGestureEl.classList.add("active");

    // Play CPU shuffle animation
    statusText.textContent = "CPU is thinking…";
    statusText.style.color = "var(--text-secondary)";
    
    const computerChoice = await shuffleCpuGesture();
    cGestureEl.textContent = emojis[computerChoice];
    cGestureEl.classList.add("active");

    const result = checkWinner(playerChoice, computerChoice);
    updateUI(playerChoice, computerChoice, result);

    setButtonsDisabled(false);
  }

  // CPU slot animation
  function shuffleCpuGesture() {
    return new Promise(resolve => {
      let ticks = 0;
      const interval = setInterval(() => {
        cGestureEl.textContent = emojis[options[ticks % 3]];
        ticks++;
      }, 80);

      setTimeout(() => {
        clearInterval(interval);
        const finalChoice = options[Math.floor(Math.random() * 3)];
        resolve(finalChoice);
      }, 700);
    });
  }

  function checkWinner(player, computer) {
    if (player === computer) return 'draw';
    
    if (
      (player === 'rock' && computer === 'scissors') ||
      (player === 'paper' && computer === 'rock') ||
      (player === 'scissors' && computer === 'paper')
    ) {
      return 'player';
    } else {
      return 'computer';
    }
  }

  function updateUI(player, computer, result) {
    if (result === 'player') {
      playerScore++;
      winStreak++;
      playerScoreEl.textContent = playerScore;
      streakValEl.textContent = winStreak;
      statusText.textContent = `Victory! ${emojis[player]} crushes ${emojis[computer]}`;
      statusText.style.color = "var(--color-green)";
    } else if (result === 'computer') {
      computerScore++;
      winStreak = 0; // reset streak
      compScoreEl.textContent = computerScore;
      streakValEl.textContent = winStreak;
      statusText.textContent = `Defeat! ${emojis[computer]} beats ${emojis[player]}`;
      statusText.style.color = "var(--color-rose)";
    } else {
      // Draw does not reset streak
      statusText.textContent = `Draw! Both selected ${emojis[player]}`;
      statusText.style.color = "var(--color-gold)";
    }
  }

  function setButtonsDisabled(disable) {
    choices.forEach(btn => btn.disabled = disable);
  }

  function resetGame() {
    playerScore = 0;
    computerScore = 0;
    winStreak = 0;
    playerScoreEl.textContent = playerScore;
    compScoreEl.textContent = computerScore;
    streakValEl.textContent = winStreak;

    pGestureEl.textContent = "❔";
    cGestureEl.textContent = "❔";
    pGestureEl.classList.remove("active");
    cGestureEl.classList.remove("active");

    statusText.textContent = 'MAKE YOUR MOVE';
    statusText.style.color = "var(--text-secondary)";
  }
})();
