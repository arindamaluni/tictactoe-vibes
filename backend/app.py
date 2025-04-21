"""
Main application file for the Tic Tac Toe game
"""
from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
from backend.api.routes import game_api
import os
import sys

# Get the absolute path to the project root directory
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(ROOT_DIR, 'frontend')

app = Flask(__name__)
CORS(app)

# Register API blueprint
app.register_blueprint(game_api, url_prefix='/api')

# Debug information route
@app.route('/debug')
def debug_info():
    return jsonify({
        'root_dir': ROOT_DIR,
        'frontend_dir': FRONTEND_DIR,
        'frontend_exists': os.path.exists(FRONTEND_DIR),
        'frontend_files': os.listdir(FRONTEND_DIR) if os.path.exists(FRONTEND_DIR) else [],
        'index_exists': os.path.exists(os.path.join(FRONTEND_DIR, 'index.html')),
        'python_path': sys.executable,
        'working_dir': os.getcwd()
    })

# Route to serve the index.html file
@app.route('/')
def index():
    return send_from_directory(FRONTEND_DIR, 'index.html')

# Route to serve static files
@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(FRONTEND_DIR, path)

if __name__ == '__main__':
    print(f"Starting server with frontend directory: {FRONTEND_DIR}")
    print(f"Frontend directory exists: {os.path.exists(FRONTEND_DIR)}")
    print(f"Index.html exists: {os.path.exists(os.path.join(FRONTEND_DIR, 'index.html'))}")
    # Use environment variable for port if available (for hosting platforms)
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=False, host='0.0.0.0', port=port)
