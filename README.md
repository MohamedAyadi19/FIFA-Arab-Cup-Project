# Arab Cup Project

A full-stack web application for managing Arab Cup tournament data, including teams, players, and matches.

## Features

- 🏆 Team management
- 👥 Player profiles and statistics
- ⚽ Match scheduling and results
- 🔐 User authentication and authorization
- 🐳 Docker containerization for easy deployment

## Tech Stack

### Backend
- **Python/Flask** - REST API framework
- **SQLAlchemy** - ORM for database management
- **JWT** - Authentication and authorization
- **Flask** - Backend Python Framework

### Frontend
- **HTML/CSS/JavaScript** - Clean and responsive UI
- **Vanilla JS** - Lightweight and fast

### Database
- **SQLite** - Development database
- **PostgreSQL** - Production-ready (configurable)

## Project Structure

```
.
├── backend/
│   ├── app.py              # Main Flask application
│   ├── models.py           # Database models
│   ├── routes/             # API endpoints
│   ├── services/           # External service integrations
│   └── requirements.txt    # Python dependencies
├── frontend/
│   ├── index.html          # Main HTML page
│   ├── app.js              # Frontend logic
│   └── style.css           # Styling
├── tests/
│   └── TESTING.md          # Testing documentation
└── docker-compose.yml      # Docker configuration
```

## Getting Started

### Prerequisites
- Python 3.8+
- Docker & Docker Compose (optional)

### Installation

#### Using Docker (Recommended)
```bash
docker-compose up --build
```

#### Manual Setup
1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   cd YOUR_REPO_NAME
   ```

2. **Set up the backend**
   ```bash
   cd backend
   pip install -r requirements.txt
   python init_db.py
   python app.py
   ```

3. **Open the frontend**
   Open `frontend/index.html` in your browser or serve it using a local web server.

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - User login

### Teams
- `GET /api/teams` - Get all teams
- `GET /api/teams/<id>` - Get team by ID
- `POST /api/teams` - Create new team
- `PUT /api/teams/<id>` - Update team
- `DELETE /api/teams/<id>` - Delete team

### Players
- `GET /api/players` - Get all players
- `GET /api/players/<id>` - Get player by ID
- `POST /api/players` - Create new player
- `PUT /api/players/<id>` - Update player
- `DELETE /api/players/<id>` - Delete player

### Matches
- `GET /api/matches` - Get all matches
- `GET /api/matches/<id>` - Get match by ID
- `POST /api/matches` - Create new match
- `PUT /api/matches/<id>` - Update match
- `DELETE /api/matches/<id>` - Delete match

## Environment Variables

Create a `.env` file in the backend directory:

```env
SECRET_KEY=your_secret_key_here
DATABASE_URL=sqlite:///arab_cup.db
FLASK_ENV=development
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the [MIT License](LICENSE).
