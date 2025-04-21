"""
Tic Tac Toe game model with AI functionality
"""
import random

class TicTacToe:
    """
    Represents a Tic Tac Toe game with all game logic and AI capabilities.
    """
    def __init__(self, ai_enabled=False, ai_player='O', difficulty='medium'):
        """Initialize an empty 3x3 board.
        
        Args:
            ai_enabled (bool): Whether AI opponent is enabled
            ai_player (str): Symbol for AI player ('X' or 'O')
            difficulty (str): AI difficulty level ('easy', 'medium', 'hard')
        """
        self.board = [[None for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.winner = None
        self.game_over = False
        self.moves_count = 0
        self.ai_enabled = ai_enabled
        self.ai_player = ai_player
        self.difficulty = difficulty

    def make_move(self, row, col):
        """
        Attempt to make a move at the specified position.
        Returns True if the move was valid and made, False otherwise.
        """
        # Check if the move is valid
        if not (0 <= row < 3 and 0 <= col < 3):
            return False
        
        # Check if the position is empty
        if self.board[row][col] is not None:
            return False
        
        # Check if the game is already over
        if self.game_over:
            return False
        
        # Make the move
        self.board[row][col] = self.current_player
        self.moves_count += 1
        
        # Check for win or draw
        self._check_game_state()
        
        # Switch player if game is not over
        if not self.game_over:
            self.current_player = 'O' if self.current_player == 'X' else 'X'
        
        return True
    
    def _check_game_state(self):
        """Check if the game has ended with a win or draw."""
        # Check rows
        for row in self.board:
            if row[0] is not None and row[0] == row[1] == row[2]:
                self.winner = row[0]
                self.game_over = True
                return

        # Check columns
        for col in range(3):
            if (self.board[0][col] is not None and 
                self.board[0][col] == self.board[1][col] == self.board[2][col]):
                self.winner = self.board[0][col]
                self.game_over = True
                return

        # Check diagonals
        if (self.board[0][0] is not None and 
            self.board[0][0] == self.board[1][1] == self.board[2][2]):
            self.winner = self.board[0][0]
            self.game_over = True
            return
            
        if (self.board[0][2] is not None and 
            self.board[0][2] == self.board[1][1] == self.board[2][0]):
            self.winner = self.board[0][2]
            self.game_over = True
            return
            
        # Check for draw
        if self.moves_count == 9:
            self.game_over = True
            # winner remains None in case of a draw
            return

    def get_state(self):
        """
        Returns the current state of the game as a dictionary.
        """
        return {
            'board': self.board,
            'currentPlayer': self.current_player,
            'winner': self.winner,
            'gameOver': self.game_over
        }

    def reset(self):
        """Reset the game to its initial state."""
        ai_enabled = getattr(self, 'ai_enabled', False)
        ai_player = getattr(self, 'ai_player', 'O')
        difficulty = getattr(self, 'difficulty', 'medium')
        self.__init__(ai_enabled, ai_player, difficulty)
        
    def make_ai_move(self):
        """
        Make a move as the AI player.
        Returns the position (row, col) where the move was made, or None if no move was made.
        """
        if self.game_over or self.current_player != self.ai_player:
            return None
            
        if self.difficulty == 'easy':
            return self._make_easy_ai_move()
        elif self.difficulty == 'medium':
            # 70% chance of making a smart move, 30% chance of random move
            if random.random() < 0.7:
                return self._make_smart_ai_move()
            else:
                return self._make_easy_ai_move()
        else:  # hard
            return self._make_smart_ai_move()
    
    def _make_easy_ai_move(self):
        """Make a random valid move."""
        empty_cells = []
        for row in range(3):
            for col in range(3):
                if self.board[row][col] is None:
                    empty_cells.append((row, col))
                    
        if empty_cells:
            row, col = random.choice(empty_cells)
            self.make_move(row, col)
            return (row, col)
        return None
    
    def _make_smart_ai_move(self):
        """Make a move using the minimax algorithm."""
        best_score = float('-inf')
        best_move = None
        
        # Find all available spots
        for row in range(3):
            for col in range(3):
                if self.board[row][col] is None:
                    # Try this move
                    self.board[row][col] = self.ai_player
                    # Calculate score from this move
                    score = self._minimax(0, False)
                    # Undo the move
                    self.board[row][col] = None
                    
                    if score > best_score:
                        best_score = score
                        best_move = (row, col)
        
        if best_move:
            row, col = best_move
            self.make_move(row, col)
            return best_move
        return None
        
    def _minimax(self, depth, is_maximizing):
        """
        Implementation of the minimax algorithm for optimal move selection.
        
        Args:
            depth (int): Current depth in the game tree
            is_maximizing (bool): Whether it's the maximizing player's turn
            
        Returns:
            int: Best score for the current board state
        """
        # Check if there's a winner
        result = self._evaluate_board()
        if result is not None:
            return result
            
        # If maximizing player (AI)
        if is_maximizing:
            best_score = float('-inf')
            for row in range(3):
                for col in range(3):
                    if self.board[row][col] is None:
                        self.board[row][col] = self.ai_player
                        score = self._minimax(depth + 1, False)
                        self.board[row][col] = None
                        best_score = max(score, best_score)
            return best_score
        
        # If minimizing player (human)
        else:
            best_score = float('inf')
            human_player = 'X' if self.ai_player == 'O' else 'O'
            for row in range(3):
                for col in range(3):
                    if self.board[row][col] is None:
                        self.board[row][col] = human_player
                        score = self._minimax(depth + 1, True)
                        self.board[row][col] = None
                        best_score = min(score, best_score)
            return best_score
    
    def _evaluate_board(self):
        """
        Evaluate the current board state for the minimax algorithm.
        
        Returns:
            int: 10 for AI win, -10 for human win, 0 for draw, None if game is ongoing
        """
        # Check rows
        for row in self.board:
            if row[0] == row[1] == row[2] and row[0] is not None:
                if row[0] == self.ai_player:
                    return 10
                return -10
                
        # Check columns
        for col in range(3):
            if (self.board[0][col] == self.board[1][col] == self.board[2][col] and 
                self.board[0][col] is not None):
                if self.board[0][col] == self.ai_player:
                    return 10
                return -10
                
        # Check diagonals
        if (self.board[0][0] == self.board[1][1] == self.board[2][2] and 
            self.board[0][0] is not None):
            if self.board[0][0] == self.ai_player:
                return 10
            return -10
            
        if (self.board[0][2] == self.board[1][1] == self.board[2][0] and 
            self.board[0][2] is not None):
            if self.board[0][2] == self.ai_player:
                return 10
            return -10
            
        # Check for draw or ongoing game
        has_empty = False
        for row in range(3):
            for col in range(3):
                if self.board[row][col] is None:
                    has_empty = True
                    break
        
        if has_empty:
            return None  # Game is ongoing
        return 0  # Draw
