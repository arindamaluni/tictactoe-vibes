"""
API routes for the Tic Tac Toe game
"""
from flask import Blueprint, jsonify, request, session
from backend.models.game import TicTacToe

# Create a blueprint for the game API
game_api = Blueprint('game_api', __name__)

# Dictionary to store game sessions (in production, use a proper database)
games = {}

@game_api.route('/new_game', methods=['POST'])
def new_game():
    """Create a new game and return its ID."""
    data = request.get_json() or {}
    
    # Check for AI settings in the request
    ai_enabled = data.get('aiEnabled', False)
    ai_player = data.get('aiPlayer', 'O')
    difficulty = data.get('difficulty', 'medium')
    
    # Validate AI player
    if ai_player not in ['X', 'O']:
        ai_player = 'O'
        
    # Validate difficulty
    if difficulty not in ['easy', 'medium', 'hard']:
        difficulty = 'medium'
    
    game_id = str(len(games) + 1)  # Simple ID generation
    games[game_id] = TicTacToe(ai_enabled=ai_enabled, ai_player=ai_player, difficulty=difficulty)
    
    game_state = games[game_id].get_state()
    
    # If AI is enabled and AI plays first (X), make the first AI move
    if ai_enabled and ai_player == 'X':
        games[game_id].make_ai_move()
        game_state = games[game_id].get_state()
    
    return jsonify({
        'gameId': game_id,
        'state': game_state,
        'aiEnabled': ai_enabled,
        'aiPlayer': ai_player,
        'difficulty': difficulty
    }), 201

@game_api.route('/game/<game_id>', methods=['GET'])
def get_game(game_id):
    """Get the current state of a game."""
    if game_id not in games:
        return jsonify({'error': 'Game not found'}), 404
    
    return jsonify({
        'gameId': game_id,
        'state': games[game_id].get_state()
    })

@game_api.route('/game/<game_id>/move', methods=['POST'])
def make_move(game_id):
    """Make a move in the specified game."""
    if game_id not in games:
        return jsonify({'error': 'Game not found'}), 404
    
    data = request.get_json()
    if not data or 'row' not in data or 'col' not in data:
        return jsonify({'error': 'Invalid move data'}), 400
    
    row = data['row']
    col = data['col']
    
    game = games[game_id]
    
    # Player's move
    if not game.make_move(row, col):
        return jsonify({
            'gameId': game_id,
            'state': game.get_state(),
            'success': False,
            'error': 'Invalid move'
        }), 400
        
    # If game is still ongoing and AI is enabled, make AI move
    ai_move = None
    if game.ai_enabled and not game.game_over:
        ai_move = game.make_ai_move()
        
    return jsonify({
        'gameId': game_id,
        'state': game.get_state(),
        'success': True,
        'aiMove': ai_move
    })

@game_api.route('/game/<game_id>/reset', methods=['POST'])
def reset_game(game_id):
    """Reset a game to its initial state."""
    if game_id not in games:
        return jsonify({'error': 'Game not found'}), 404
    
    games[game_id].reset()
    
    return jsonify({
        'gameId': game_id,
        'state': games[game_id].get_state(),
        'message': 'Game reset successfully'
    })
