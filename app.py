"""
Entry point for the Tic Tac Toe application
"""
import os
from backend.app import create_app

# Create the Flask application
app = create_app()

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
