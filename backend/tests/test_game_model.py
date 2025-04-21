"""
Unit tests for the Tic Tac Toe game model
"""
import pytest
from backend.models.game import TicTacToe

def test_game_initialization():
    """Test that the game initializes correctly."""
    game = TicTacToe()
    assert game.board == [[None, None, None], [None, None, None], [None, None, None]]
    assert game.current_player == 'X'
    assert game.winner is None
    assert game.game_over is False
    assert game.moves_count == 0

def test_make_valid_move():
    """Test making a valid move."""
    game = TicTacToe()
    result = game.make_move(0, 0)
    assert result is True
    assert game.board[0][0] == 'X'
    assert game.current_player == 'O'
    assert game.moves_count == 1

def test_make_invalid_move():
    """Test making an invalid move."""
    game = TicTacToe()
    # Make a move first
    game.make_move(0, 0)
    # Try to make a move in the same position
    result = game.make_move(0, 0)
    assert result is False
    # Check that the game state hasn't changed
    assert game.board[0][0] == 'X'
    assert game.current_player == 'O'
    assert game.moves_count == 1

def test_out_of_bounds_move():
    """Test making a move outside the board boundaries."""
    game = TicTacToe()
    result = game.make_move(3, 3)
    assert result is False
    assert game.moves_count == 0

def test_horizontal_win():
    """Test winning with a horizontal line."""
    game = TicTacToe()
    # X makes moves
    game.make_move(0, 0)  # X at (0,0)
    # O makes move
    game.make_move(1, 0)  # O at (1,0)
    # X makes move
    game.make_move(0, 1)  # X at (0,1)
    # O makes move
    game.make_move(1, 1)  # O at (1,1)
    # X makes move
    game.make_move(0, 2)  # X at (0,2)
    
    assert game.game_over is True
    assert game.winner == 'X'

def test_vertical_win():
    """Test winning with a vertical line."""
    game = TicTacToe()
    # X makes moves
    game.make_move(0, 0)  # X at (0,0)
    # O makes move
    game.make_move(0, 1)  # O at (0,1)
    # X makes move
    game.make_move(1, 0)  # X at (1,0)
    # O makes move
    game.make_move(1, 1)  # O at (1,1)
    # X makes move
    game.make_move(2, 0)  # X at (2,0)
    
    assert game.game_over is True
    assert game.winner == 'X'

def test_diagonal_win():
    """Test winning with a diagonal line."""
    game = TicTacToe()
    # X makes moves
    game.make_move(0, 0)  # X at (0,0)
    # O makes move
    game.make_move(0, 1)  # O at (0,1)
    # X makes move
    game.make_move(1, 1)  # X at (1,1)
    # O makes move
    game.make_move(0, 2)  # O at (0,2)
    # X makes move
    game.make_move(2, 2)  # X at (2,2)
    
    assert game.game_over is True
    assert game.winner == 'X'

def test_draw_game():
    """Test a drawn game where neither player wins."""
    game = TicTacToe()
    # Fill the board in a way that no one wins
    # X | O | X
    # O | X | O
    # O | X | O
    moves = [
        (0, 0), (0, 1), (0, 2),
        (1, 1), (1, 0), (1, 2),
        (2, 1), (2, 0), (2, 2)
    ]
    
    for row, col in moves:
        game.make_move(row, col)
    
    assert game.game_over is True
    assert game.winner is None
    assert game.moves_count == 9

def test_reset_game():
    """Test resetting the game."""
    game = TicTacToe()
    # Make some moves
    game.make_move(0, 0)
    game.make_move(0, 1)
    
    # Reset the game
    game.reset()
    
    # Check that the game state is back to initial
    assert game.board == [[None, None, None], [None, None, None], [None, None, None]]
    assert game.current_player == 'X'
    assert game.winner is None
    assert game.game_over is False
    assert game.moves_count == 0
