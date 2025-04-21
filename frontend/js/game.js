/**
 * Tic Tac Toe Game Frontend Logic
 */

// API endpoint base URL - using relative path to work in both local and production environments
const API_BASE_URL = '/api';

// Game state
let gameState = {
    gameId: null,
    board: null,
    currentPlayer: 'X',
    winner: null,
    gameOver: false
};

// AI settings
let aiSettings = {
    aiEnabled: true,
    aiPlayer: 'O',
    difficulty: 'medium'
};

// DOM Elements
const gameStatusElement = document.getElementById('game-status');
const currentPlayerElement = document.getElementById('current-player');
const cells = document.querySelectorAll('.cell');
const resetButton = document.getElementById('reset-game');

// AI settings elements
const aiEnabledCheckbox = document.getElementById('ai-enabled');
const aiPlayerSelect = document.getElementById('ai-player');
const difficultySelect = document.getElementById('difficulty');
const applySettingsButton = document.getElementById('apply-settings');

/**
 * Initialize a new game
 */
async function initGame() {
    try {
        const response = await fetch(`${API_BASE_URL}/new_game`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                aiEnabled: aiSettings.aiEnabled,
                aiPlayer: aiSettings.aiPlayer,
                difficulty: aiSettings.difficulty
            })
        });
        
        if (!response.ok) {
            throw new Error('Failed to create new game');
        }
        
        const data = await response.json();
        gameState = {
            gameId: data.gameId,
            ...data.state
        };
        
        // Save AI settings from the response
        aiSettings = {
            aiEnabled: data.aiEnabled,
            aiPlayer: data.aiPlayer,
            difficulty: data.difficulty
        };
        
        updateUI();
    } catch (error) {
        console.error('Error initializing game:', error);
        gameStatusElement.textContent = 'Error starting game. Please refresh the page.';
    }
}

/**
 * Make a move on the board
 * @param {number} row - Row index (0-2)
 * @param {number} col - Column index (0-2)
 */
async function makeMove(row, col) {
    if (gameState.gameOver || gameState.board[row][col] !== null) {
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/game/${gameState.gameId}/move`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ row, col })
        });
        
        const data = await response.json();
        
        if (response.ok && data.success) {
            gameState = {
                gameId: data.gameId,
                ...data.state
            };
            updateUI();
            
            // If AI made a move, highlight it briefly
            if (data.aiMove) {
                const [aiRow, aiCol] = data.aiMove;
                const aiCell = document.querySelector(`.cell[data-row="${aiRow}"][data-col="${aiCol}"]`);
                if (aiCell) {
                    aiCell.classList.add('ai-move');
                    setTimeout(() => {
                        aiCell.classList.remove('ai-move');
                    }, 1000);
                }
            }
        }
    } catch (error) {
        console.error('Error making move:', error);
    }
}

/**
 * Reset the current game
 */
async function resetGame() {
    // Remove any existing winner message before resetting
    const existingAnnouncement = document.querySelector('.winner-message');
    if (existingAnnouncement) {
        existingAnnouncement.remove();
    }
    
    if (gameState.gameId) {
        try {
            const response = await fetch(`${API_BASE_URL}/game/${gameState.gameId}/reset`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            
            if (!response.ok) {
                throw new Error('Failed to reset game');
            }
            
            const data = await response.json();
            gameState = {
                gameId: data.gameId,
                ...data.state
            };
            
            updateUI();
        } catch (error) {
            console.error('Error resetting game:', error);
        }
    } else {
        initGame();
    }
}

/**
 * Apply settings and start a new game
 */
function applySettings() {
    aiSettings = {
        aiEnabled: aiEnabledCheckbox.checked,
        aiPlayer: aiPlayerSelect.value,
        difficulty: difficultySelect.value
    };
    
    initGame();
}

/**
 * Find winning cells if there's a winner
 * Returns an array of winning cell coordinates or null if there's no winner
 */
function findWinningCells() {
    if (!gameState.winner) return null;
    
    const board = gameState.board;
    const winPatterns = [
        // Rows
        [[0,0], [0,1], [0,2]],
        [[1,0], [1,1], [1,2]],
        [[2,0], [2,1], [2,2]],
        // Columns
        [[0,0], [1,0], [2,0]],
        [[0,1], [1,1], [2,1]],
        [[0,2], [1,2], [2,2]],
        // Diagonals
        [[0,0], [1,1], [2,2]],
        [[0,2], [1,1], [2,0]]
    ];
    
    // Check each winning pattern
    for (const pattern of winPatterns) {
        const [a, b, c] = pattern;
        if (board[a[0]][a[1]] && 
            board[a[0]][a[1]] === board[b[0]][b[1]] && 
            board[a[0]][a[1]] === board[c[0]][c[1]]) {
            return pattern; // Return the winning cells
        }
    }
    
    return null;
}

/**
 * Create a stylish winner announcement element
 */
function createWinnerAnnouncement() {
    // Remove any existing announcement
    const existingAnnouncement = document.querySelector('.winner-message');
    if (existingAnnouncement) {
        existingAnnouncement.remove();
    }
    
    // Create new announcement
    const announcement = document.createElement('div');
    announcement.classList.add('winner-message');
    
    if (gameState.winner === 'X') {
        announcement.classList.add('winner-x');
        announcement.innerHTML = '🎉 Player <strong>X</strong> Wins! 🎉';
    } else if (gameState.winner === 'O') {
        announcement.classList.add('winner-o');
        announcement.innerHTML = '🎉 Player <strong>O</strong> Wins! 🎉';
    } else {
        announcement.classList.add('winner-draw');
        announcement.textContent = "It's a Draw!";
    }
    
    // Insert after game-info
    const gameInfo = document.querySelector('.game-info');
    gameInfo.after(announcement);
    
    return announcement;
}

/**
 * Create confetti effect when someone wins
 */
function createConfetti() {
    const colors = gameState.winner === 'X' ? 
        ['#4285f4', '#8ab4f8', '#c6dafc'] : 
        ['#ea4335', '#f28b82', '#fad2cf'];
    
    // Create confetti elements
    for (let i = 0; i < 100; i++) {
        const confetti = document.createElement('div');
        confetti.style.position = 'absolute';
        confetti.style.width = Math.random() * 10 + 5 + 'px';
        confetti.style.height = Math.random() * 10 + 5 + 'px';
        confetti.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
        confetti.style.borderRadius = Math.random() > 0.5 ? '50%' : '0';
        confetti.style.left = Math.random() * 100 + '%';
        confetti.style.top = -20 + 'px';
        confetti.style.opacity = Math.random() + 0.5;
        confetti.style.zIndex = '1000';
        confetti.style.transform = `rotate(${Math.random() * 360}deg)`;
        confetti.style.animation = `fall ${Math.random() * 3 + 2}s linear forwards`;
        
        document.querySelector('.game-board').appendChild(confetti);
        
        // Clean up confetti after animation
        setTimeout(() => {
            confetti.remove();
        }, 5000);
    }
}

/**
 * Update the UI based on the current game state
 */
function updateUI() {
    // Remove any previous winning classes
    cells.forEach(cell => cell.classList.remove('winning'));
    
    // Update board cells
    cells.forEach(cell => {
        const row = parseInt(cell.dataset.row);
        const col = parseInt(cell.dataset.col);
        const value = gameState.board[row][col];
        
        cell.textContent = value || '';
        cell.classList.remove('x', 'o');
        
        if (value) {
            cell.classList.add(value.toLowerCase());
        }
    });
    
    // Handle game state and winner display
    if (gameState.gameOver) {
        // Remove any existing winner message
        const existingMessage = document.querySelector('.winner-message');
        if (existingMessage) {
            existingMessage.remove();
        }
        
        if (gameState.winner) {
            // Find and highlight winning cells
            const winningCells = findWinningCells();
            if (winningCells) {
                winningCells.forEach(([row, col]) => {
                    const cell = document.querySelector(`.cell[data-row="${row}"][data-col="${col}"]`);
                    if (cell) {
                        cell.classList.add('winning');
                    }
                });
                
                // Create winner announcement
                createWinnerAnnouncement();
                
                // Add confetti effect
                createConfetti();
                
                // Update game status message
                gameStatusElement.textContent = `Player ${gameState.winner} wins!`;
            }
        } else {
            // It's a draw
            gameStatusElement.textContent = "It's a draw!";
            createWinnerAnnouncement();
        }
    } else {
        // Game is still ongoing
        gameStatusElement.textContent = `Player ${gameState.currentPlayer}'s turn`;
        currentPlayerElement.textContent = gameState.currentPlayer;
    }
}

/**
 * Event Listeners
 */
// Cell click event
cells.forEach(cell => {
    cell.addEventListener('click', () => {
        const row = parseInt(cell.dataset.row);
        const col = parseInt(cell.dataset.col);
        makeMove(row, col);
    });
});

// Reset button click event
resetButton.addEventListener('click', resetGame);

// Apply Settings button click event
applySettingsButton.addEventListener('click', applySettings);

// Load existing settings on page load
function loadSettings() {
    aiEnabledCheckbox.checked = aiSettings.aiEnabled;
    aiPlayerSelect.value = aiSettings.aiPlayer;
    difficultySelect.value = aiSettings.difficulty;
}

// Initialize the game when the page loads
document.addEventListener('DOMContentLoaded', () => {
    loadSettings();
    initGame();
});
