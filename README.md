# Web-based Tic Tac Toe Game

A clean, minimalist web-based Tic Tac Toe game with Python backend and JavaScript frontend. The game features a Google-inspired design with a clear separation between frontend and backend components to allow for future AI integration.

## Features

- Clean, minimalist UI inspired by Google's design principles
- Responsive design that works on desktop and mobile
- RESTful API backend built with Flask
- Separate game logic from presentation
- Well-structured code with comprehensive tests
- Ready for future AI integration

## Project Structure

```
tic/
├── backend/            # Python Flask backend
│   ├── api/            # API endpoints
│   ├── models/         # Game logic and models
│   ├── tests/          # Unit tests
│   └── app.py          # Main application file
├── frontend/           # Frontend assets
│   ├── css/            # Stylesheets
│   ├── js/             # JavaScript files
│   └── index.html      # Main HTML file
└── venv/               # Python virtual environment
```

## Prerequisites

- Python 3.7 or higher
- Web browser with JavaScript enabled

## Installation

1. Clone this repository:
   ```
   git clone <repository-url>
   cd tic
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Running the Application

1. Start the Flask backend server:
   ```
   python -m backend.app
   ```

2. Open your web browser and navigate to:
   ```
   http://localhost:5000
   ```

## Running the Tests

To run the unit tests:

```
pytest
```

## API Endpoints

- `POST /api/new_game` - Create a new game
- `GET /api/game/<game_id>` - Get the current state of a game
- `POST /api/game/<game_id>/move` - Make a move in a game
- `POST /api/game/<game_id>/reset` - Reset a game to its initial state

## Future Enhancements

- AI opponent using minimax algorithm
- User accounts and game history
- Multiplayer functionality
- Game statistics

## License

MIT

## Author

Created by [Your Name]
