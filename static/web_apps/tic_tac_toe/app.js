/* ═══════════════════════════════════════════════════════════════════════════
   Sinter Toe — JavaScript Logic
   ═══════════════════════════════════════════════════════════════════════════ */

(() => {
  "use strict";

  const cells       = document.querySelectorAll('.cell');
  const statusText    = document.getElementById('status');
  const statusBadge   = document.getElementById('status-badge');
  const resetBtn      = document.getElementById('reset-btn');

  // Stats
  const scoreXEl      = document.getElementById('wins-x');
  const scoreOEl      = document.getElementById('wins-o');
  const scoreDrawEl   = document.getElementById('draws-val');

  let board = ['', '', '', '', '', '', '', '', ''];
  let currentPlayer = 'X';
  let running = false;

  let scoreX = 0;
  let scoreO = 0;
  let scoreDraw = 0;

  const winConditions = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8], // Rows
    [0, 3, 6], [1, 4, 7], [2, 5, 8], // Cols
    [0, 4, 8], [2, 4, 6]             // Diagonals
  ];

  // SVG strings for X and O
  const svgX = `
    <svg viewBox="0 0 100 100">
      <line x1="20" y1="20" x2="80" y2="80" class="symbol-path" />
      <line x1="80" y1="20" x2="20" y2="80" class="symbol-path" style="animation-delay: 0.15s" />
    </svg>
  `;

  const svgO = `
    <svg viewBox="0 0 100 100">
      <circle cx="50" cy="50" r="30" class="symbol-path" />
    </svg>
  `;

  initializeGame();

  function initializeGame() {
    cells.forEach(cell => cell.addEventListener('click', cellClicked));
    resetBtn.addEventListener('click', restartGame);
    updateStatus();
    running = true;
  }

  function cellClicked() {
    const cellIndex = this.getAttribute('data-index');
    if (board[cellIndex] !== '' || !running) return;

    updateCell(this, cellIndex);
    checkWinner();
  }

  function updateCell(cell, index) {
    board[index] = currentPlayer;
    cell.innerHTML = currentPlayer === 'X' ? svgX : svgO;
    cell.classList.add(currentPlayer.toLowerCase());
  }

  function changePlayer() {
    currentPlayer = (currentPlayer === 'X') ? 'O' : 'X';
    updateStatus();
  }

  function updateStatus(overrideText = null, isFinal = false, statusType = null) {
    if (overrideText) {
      statusText.textContent = overrideText;
      statusBadge.className = "status-badge";
      if (statusType) {
        statusBadge.classList.add(statusType);
      }
      return;
    }

    statusText.textContent = `Player ${currentPlayer}'s Turn`;
    statusBadge.className = "status-badge";
    if (currentPlayer === 'O') {
      statusBadge.classList.add("player-o");
    }
  }

  function checkWinner() {
    let roundWon = false;
    let winningCombo = [];

    for (let i = 0; i < winConditions.length; i++) {
      const condition = winConditions[i];
      const cellA = board[condition[0]];
      const cellB = board[condition[1]];
      const cellC = board[condition[2]];

      if (cellA === '' || cellB === '' || cellC === '') continue;
      
      if (cellA === cellB && cellB === cellC) {
        roundWon = true;
        winningCombo = condition;
        break;
      }
    }

    if (roundWon) {
      highlightWinningCells(winningCombo);
      updateStatus(`🎉 Player ${currentPlayer} Wins!`, true, currentPlayer === 'X' ? '' : 'player-o');
      
      if (currentPlayer === 'X') {
        scoreX++;
        scoreXEl.textContent = scoreX;
      } else {
        scoreO++;
        scoreOEl.textContent = scoreO;
      }
      
      running = false;
    } else if (!board.includes('')) {
      updateStatus(`Draw!`, true, 'draw');
      scoreDraw++;
      scoreDrawEl.textContent = scoreDraw;
      running = false;
    } else {
      changePlayer();
    }
  }

  function highlightWinningCells(combo) {
    combo.forEach(idx => {
      cells[idx].classList.add("winner");
    });
  }

  function restartGame() {
    currentPlayer = 'X';
    board = ['', '', '', '', '', '', '', '', ''];
    updateStatus();
    cells.forEach(cell => {
      cell.innerHTML = '';
      cell.className = 'cell';
    });
    running = true;
  }
})();
