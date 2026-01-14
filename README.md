# FIFA Arab Cup - Web Services Project

A comprehensive REST API-based web application for managing FIFA Arab Cup tournament data, implementing modern web service architecture principles for academic demonstration purposes.

## Project Overview

This project is an academic implementation of a RESTful web service designed to manage tournament information for the FIFA Arab Cup. The system provides a complete backend API for managing teams, players, matches, and user authentication, along with a frontend client that consumes these services.

**Project Objectives:**
- Demonstrate REST API design principles and best practices
- Implement secure authentication and authorization using JWT
- Design and implement a normalized relational database schema
- Provide a clean separation between backend services and frontend clients
- Showcase containerization and deployment using Docker

**Scope:**
The application manages the core entities of a football tournament: teams participating in the Arab Cup, players associated with these teams, match schedules and results, and user accounts for system access control.

## Features

- 🏆 **Team Management** - CRUD operations for tournament teams
- 👥 **Player Profiles** - Detailed player information and statistics
- ⚽ **Match Scheduling** - Match data including scores, dates, and venues
- 🔐 **JWT Authentication** - Secure token-based user authentication
- 🔒 **Protected Endpoints** - Authorization-controlled API access
- 🐳 **Docker Deployment** - Containerized application with database
- 📊 **RESTful Architecture** - Standard HTTP methods and status codes

## Tech Stack

### Backend
- **Python 3.8+** - Programming language
- **Flask** - Lightweight web framework for REST API
- **SQLAlchemy** - Object-Relational Mapping (ORM) for database operations
- **Flask-JWT-Extended** - JWT token generation and validation
- **Flask-CORS** - Cross-Origin Resource Sharing support
- **python-dotenv** - Environment variable management

### Frontend
- **HTML5** - Markup structure
- **CSS3** - Styling and responsive design
- **Vanilla JavaScript** - Client-side logic and API consumption
- **Fetch API** - HTTP requests to backend

### Database
- **SQLite** - Development database (file-based, zero configuration)
- **PostgreSQL** - Production database (Docker containerized)

### DevOps & Tools
- **Docker & Docker Compose** - Containerization and orchestration
- **Git** - Version control

---

## System Architecture

The application follows a **three-tier architecture** with clear separation of concerns:

```
┌─────────────────────────────────────────────────────────────┐
│                         FRONTEND                             │
│  ┌────────────────────────────────────────────────────┐     │
│  │   HTML + CSS + JavaScript (Client)                  │     │
│  │   - User Interface                                  │     │
│  │   - API Consumption via Fetch                       │     │
│  │   - JWT Token Storage (localStorage)                │     │
│  └────────────────────────────────────────────────────┘     │
└──────────────────────────┬──────────────────────────────────┘
                           │ HTTP/JSON
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    BACKEND (Flask API)                       │
│  ┌────────────────────────────────────────────────────┐     │
│  │  Routes Layer (API Endpoints)                       │     │
│  │  - /api/auth/*    - /api/teams/*                    │     │
│  │  - /api/players/* - /api/matches/*                  │     │
│  └────────────────────────────────────────────────────┘     │
│  ┌────────────────────────────────────────────────────┐     │
│  │  Security Layer                                     │     │
│  │  - JWT Token Validation                             │     │
│  │  - @token_required Decorator                        │     │
│  └────────────────────────────────────────────────────┘     │
│  ┌────────────────────────────────────────────────────┐     │
│  │  Business Logic Layer                               │     │
│  │  - CRUD Operations                                  │     │
│  │  - Data Validation                                  │     │
│  └────────────────────────────────────────────────────┘     │
│  ┌────────────────────────────────────────────────────┐     │
│  │  Data Access Layer (SQLAlchemy ORM)                 │     │
│  │  - Models: User, Team, Player, Match                │     │
│  └────────────────────────────────────────────────────┘     │
└──────────────────────────┬──────────────────────────────────┘
                           │ SQL Queries
                           ▼
┌─────────────────────────────────────────────────────────────┐
│              DATABASE (PostgreSQL/SQLite)                    │
│  ┌────────────────────────────────────────────────────┐     │
│  │   Tables: users, teams, players, matches            │     │
│  │   - Relational schema with foreign keys            │     │
│  │   - Data persistence and integrity                 │     │
│  └────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow

1. **Client Request**: Frontend sends HTTP request (GET, POST, PUT, DELETE) with JSON payload
2. **Authentication**: Flask middleware checks for JWT token in protected routes
3. **Authorization**: Token is validated, user identity is verified
4. **Business Logic**: Route handler processes request, validates data
5. **Database Operation**: SQLAlchemy ORM executes database query
6. **Response**: JSON response sent back to client with appropriate HTTP status code

---

## API Design

### REST Principles

This API follows RESTful design principles:

- **Resource-Based URLs**: Each endpoint represents a resource (`/teams`, `/players`, `/matches`)
- **HTTP Methods**: Standard verbs for operations (GET, POST, PUT, DELETE)
- **Stateless**: Each request contains all necessary information (via JWT token)
- **JSON Format**: All data exchanged in JSON format
- **HTTP Status Codes**: Proper use of status codes (200, 201, 400, 401, 404, 500)

### Resource Structure

#### 1. Authentication Resources

**POST /api/auth/login**
- **Purpose**: Authenticate user and receive JWT token
- **Request Body**:
```json
{
  "username": "admin",
  "password": "password123"
}
```
- **Response** (200 OK):
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```
- **Error Response** (401 Unauthorized):
```json
{
  "error": "Invalid credentials"
}
```

#### 2. Team Resources

**GET /api/teams**
- **Purpose**: Retrieve all teams
- **Authentication**: Required
- **Response** (200 OK):
```json
[
  {
    "id": 1,
    "team_id": "12345",
    "name": "Egypt",
    "country": "Egypt",
    "badge": "https://example.com/egypt.png"
  },
  {
    "id": 2,
    "team_id": "12346",
    "name": "Morocco",
    "country": "Morocco",
    "badge": "https://example.com/morocco.png"
  }
]
```

**GET /api/teams/{id}**
- **Purpose**: Retrieve single team by ID
- **Authentication**: Required
- **Response** (200 OK):
```json
{
  "id": 1,
  "team_id": "12345",
  "name": "Egypt",
  "country": "Egypt",
  "badge": "https://example.com/egypt.png"
}
```

**POST /api/teams**
- **Purpose**: Create new team
- **Authentication**: Required
- **Request Body**:
```json
{
  "team_id": "12347",
  "name": "Tunisia",
  "country": "Tunisia",
  "badge": "https://example.com/tunisia.png"
}
```
- **Response** (201 Created):
```json
{
  "message": "Team created successfully",
  "id": 3
}
```

**PUT /api/teams/{id}**
- **Purpose**: Update existing team
- **Authentication**: Required

**DELETE /api/teams/{id}**
- **Purpose**: Delete team
- **Authentication**: Required
- **Response** (200 OK):
```json
{
  "message": "Team deleted successfully"
}
```

#### 3. Player Resources

**GET /api/players**
- **Purpose**: Retrieve all players
- **Authentication**: Required
- **Response** (200 OK):
```json
[
  {
    "id": 1,
    "player_id": "P001",
    "name": "Mohamed Salah",
    "position": "Forward",
    "nationality": "Egypt",
    "date_of_birth": "1992-06-15",
    "height": "175 cm",
    "team_id": 1
  }
]
```

**POST /api/players**
- **Purpose**: Create new player
- **Authentication**: Required
- **Request Body**:
```json
{
  "player_id": "P002",
  "name": "Achraf Hakimi",
  "position": "Defender",
  "nationality": "Morocco",
  "date_of_birth": "1998-11-04",
  "height": "181 cm",
  "team_id": 2
}
```

#### 4. Match Resources

**GET /api/matches**
- **Purpose**: Retrieve all matches
- **Authentication**: Required
- **Response** (200 OK):
```json
[
  {
    "id": 1,
    "event_id": "M001",
    "season": "2021",
    "date": "2021-11-30",
    "home_team": "Egypt",
    "away_team": "Morocco",
    "home_team_id": 1,
    "away_team_id": 2,
    "home_score": 2,
    "away_score": 1,
    "venue": "Al Bayt Stadium"
  }
]
```

---

## Security

### JWT Authentication

The application implements **JSON Web Token (JWT)** authentication for secure, stateless user sessions.

#### How It Works

1. **User Login**: Client sends username and password to `/api/auth/login`
2. **Token Generation**: Server validates credentials and generates JWT containing:
   - `user_id`: Identifies the user
   - `exp`: Expiration timestamp (2 hours from issue time)
   - Signature: HMAC-SHA256 signature using secret key
3. **Token Storage**: Client stores token (typically in `localStorage`)
4. **Protected Requests**: Client includes token in `Authorization` header:
   ```
   Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
   ```
5. **Token Validation**: Server validates token on each protected endpoint request

#### Implementation Details

**Token Generation** (`auth_utils.py`):
```python
def generate_token(user_id):
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(hours=2)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")
```

**Token Validation Decorator**:
```python
@token_required
def protected_route():
    # This route requires valid JWT token
    pass
```

#### Protected Endpoints

All endpoints except `/api/auth/login` require valid JWT token:
- ✅ `POST /api/auth/login` - Public
- 🔒 `GET /api/teams` - Protected
- 🔒 `POST /api/teams` - Protected
- 🔒 `GET /api/players` - Protected
- 🔒 `GET /api/matches` - Protected
- 🔒 All other CRUD operations - Protected

#### Security Considerations

- **Token Expiration**: Tokens expire after 2 hours to limit exposure
- **Secret Key**: Stored in environment variables, never in code
- **HTTPS**: Should be used in production to prevent token interception
- **Password Storage**: Currently plain text (⚠️ see Limitations section)

---

## Database Design

### Entity-Relationship Model

The database follows a **normalized relational schema** with four main entities:

```
┌─────────────────┐
│     USERS       │
│─────────────────│
│ id (PK)         │
│ username        │
│ password        │
└─────────────────┘

┌─────────────────┐         ┌─────────────────┐
│     TEAMS       │         │    PLAYERS      │
│─────────────────│         │─────────────────│
│ id (PK)         │◄───────┐│ id (PK)         │
│ team_id (UQ)    │        ││ player_id (UQ)  │
│ name            │        ││ name            │
│ country         │        ││ position        │
│ badge           │        ││ nationality     │
└─────────────────┘        ││ date_of_birth   │
        ▲                  ││ height          │
        │                  ││ team_id (FK)    │
        │                  │└─────────────────┘
        │                  │
        │                  │
┌───────┴─────────┐        │
│    MATCHES      │        │
│─────────────────│        │
│ id (PK)         │        │
│ event_id (UQ)   │        │
│ season          │        │
│ date            │        │
│ home_team       │        │
│ away_team       │        │
│ home_team_id(FK)├────────┘
│ away_team_id(FK)├────────┐
│ home_score      │        │
│ away_score      │        │
│ venue           │        │
└─────────────────┘        │
                           │
                           ▼
                  (References TEAMS)
```

### Database Schema

#### Users Table
- **Purpose**: Store user credentials for authentication
- **Fields**:
  - `id`: Primary key
  - `username`: Unique username (50 chars)
  - `password`: User password (200 chars)

#### Teams Table
- **Purpose**: Store team information
- **Fields**:
  - `id`: Primary key (auto-increment)
  - `team_id`: Unique external identifier (from API sources)
  - `name`: Team name (100 chars)
  - `country`: Country name (100 chars)
  - `badge`: URL to team logo (255 chars)

#### Players Table
- **Purpose**: Store player information
- **Fields**:
  - `id`: Primary key
  - `player_id`: Unique external identifier
  - `name`: Player name (100 chars)
  - `position`: Playing position (50 chars)
  - `nationality`: Player nationality (50 chars)
  - `date_of_birth`: Birth date (string format)
  - `height`: Player height (50 chars)
  - `team_id`: Foreign key to Teams table

**Relationship**: Many-to-One (Many players belong to one team)

#### Matches Table
- **Purpose**: Store match information and results
- **Fields**:
  - `id`: Primary key
  - `event_id`: Unique match identifier
  - `season`: Tournament season (20 chars)
  - `date`: Match date (string format)
  - `home_team`: Home team name (100 chars)
  - `away_team`: Away team name (100 chars)
  - `home_team_id`: Foreign key to Teams table
  - `away_team_id`: Foreign key to Teams table
  - `home_score`: Home team score
  - `away_score`: Away team score
  - `venue`: Match venue (100 chars)

**Relationships**: 
- Two Many-to-One relationships (home team and away team reference Teams)

### Why Relational Database?

A relational database was chosen for this project because:

1. **Data Integrity**: Foreign key constraints ensure referential integrity (e.g., players cannot reference non-existent teams)
2. **ACID Properties**: Transactions ensure data consistency
3. **Structured Data**: Tournament data has clear structure and relationships
4. **Query Flexibility**: SQL enables complex queries (e.g., "all players from teams in a specific match")
5. **Normalization**: Reduces data redundancy (team info stored once, referenced by players and matches)
6. **Academic Relevance**: Demonstrates understanding of database design principles

---

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
- **Python 3.8+** - Backend runtime
- **pip** - Python package manager
- **Docker & Docker Compose** (optional) - For containerized deployment
- **Git** - Version control

### Installation

#### Option 1: Using Docker (Recommended)

Docker provides a consistent environment with all dependencies configured.

```bash
# Clone the repository
git clone https://github.com/MohamedAyadi19/FIFA-Arab-Cup-Project.git
cd FIFA-Arab-Cup-Project

# Create .env file (see Environment Variables section)
# Then start all services
docker-compose up --build
```

The application will be available at `http://localhost:5000`

#### Option 2: Manual Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/MohamedAyadi19/FIFA-Arab-Cup-Project.git
   cd FIFA-Arab-Cup-Project
   ```

2. **Set up Python virtual environment** (recommended)
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install backend dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   
   Create a `.env` file in the project root:
   ```env
   SECRET_KEY=your_secret_key_here_change_in_production
   DATABASE_URL=sqlite:///arab_cup.db
   FLASK_ENV=development
   ```

5. **Initialize the database**
   ```bash
   python init_db.py
   ```

6. **Run the Flask application**
   ```bash
   python app.py
   ```

7. **Access the application**
   
   Open your browser and navigate to `http://localhost:5000`

---

## Testing

### Testing Approach

The project includes both **manual** and **automated** testing strategies:

#### Manual API Testing

**Tools**: Postman, cURL, or browser-based tools

Example tests using cURL:

1. **Login Test**:
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"password123"}'
```

Expected: JWT token in response

2. **Get All Teams (Protected)**:
```bash
curl -X GET http://localhost:5000/api/teams \
  -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE"
```

Expected: JSON array of teams

3. **Create Team (Protected)**:
```bash
curl -X POST http://localhost:5000/api/teams \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE" \
  -d '{"team_id":"T123","name":"Algeria","country":"Algeria","badge":"https://example.com/algeria.png"}'
```

Expected: 201 Created with success message

#### Automated Testing

Automated tests are documented in [`tests/TESTING.md`](tests/TESTING.md).

**Test Categories**:
- **Unit Tests**: Test individual functions and methods
- **Integration Tests**: Test API endpoints and database interactions
- **Authentication Tests**: Verify JWT token generation and validation
- **Authorization Tests**: Ensure protected routes reject invalid tokens
- **CRUD Tests**: Verify Create, Read, Update, Delete operations

**Test Coverage Areas**:
- ✅ User authentication (login with valid/invalid credentials)
- ✅ JWT token validation (expired, missing, invalid tokens)
- ✅ CRUD operations for teams, players, matches
- ✅ Database constraints (unique fields, foreign keys)
- ✅ Error handling (404, 401, 400, 500 responses)
- ✅ CORS headers for cross-origin requests

---

## Deployment & Configuration

### Docker Deployment

The application uses **Docker Compose** to orchestrate multiple services:

**Services Defined** (`docker-compose.yml`):

1. **PostgreSQL Database**
   - Image: `postgres:15`
   - Port: `5432`
   - Volume: Persistent data storage
   - Environment: Database credentials

2. **Flask Backend**
   - Build: Custom Dockerfile
   - Port: `5000`
   - Depends on: PostgreSQL service
   - Environment: Loaded from `.env` file

**Benefits of Docker**:
- **Consistency**: Same environment across development and production
- **Isolation**: Dependencies contained, no system pollution
- **Portability**: Deploy anywhere Docker runs
- **Scalability**: Easy to add replicas or services

### Environment Variables

**Required Variables** (`.env` file):

```env
# Security
SECRET_KEY=your_secret_key_minimum_32_characters_random_string

# Database Configuration
DATABASE_URL=postgresql://postgres:postgres@db:5432/arab_cup

# Flask Configuration
FLASK_ENV=development
FLASK_APP=app.py
```

**Development vs Production**:

| Variable | Development | Production |
|----------|------------|------------|
| `SECRET_KEY` | Simple string | Strong random key (32+ chars) |
| `DATABASE_URL` | SQLite file | PostgreSQL connection string |
| `FLASK_ENV` | `development` | `production` |

⚠️ **Security Note**: Never commit `.env` file to version control. Use `.env.example` template instead.

### Database Configuration

**SQLite** (Development):
```env
DATABASE_URL=sqlite:///arab_cup.db
```
- File-based, zero configuration
- Stored in backend directory
- Suitable for development and testing

**PostgreSQL** (Production):
```env
DATABASE_URL=postgresql://user:password@host:port/database
```
- Client-server architecture
- Better performance and concurrency
- ACID compliance and advanced features

---

## Project Structure

```
.
├── backend/
│   ├── app.py                    # Flask application factory
│   ├── models.py                 # SQLAlchemy database models
│   ├── extensions.py             # Flask extensions (SQLAlchemy)
│   ├── auth_utils.py             # JWT utilities and decorators
│   ├── init_db.py                # Database initialization script
│   ├── seed_players.py           # Data seeding script
│   ├── requirements.txt          # Python dependencies
│   ├── Dockerfile                # Docker container definition
│   ├── routes/
│   │   ├── __init__.py           # Routes package initializer
│   │   ├── auth.py               # Authentication endpoints
│   │   ├── teams.py              # Team CRUD endpoints
│   │   ├── players.py            # Player CRUD endpoints
│   │   └── matches.py            # Match CRUD endpoints
│   └── services/
│       └── sportsdb_service.py   # External API integration
├── frontend/
│   ├── index.html                # Main HTML page
│   ├── app.js                    # Frontend JavaScript logic
│   └── style.css                 # CSS styling
├── tests/
│   └── TESTING.md                # Testing documentation
├── docker-compose.yml            # Docker orchestration
├── .env                          # Environment variables (not in repo)
├── .gitignore                    # Git ignore rules
└── README.md                     # This file
```

---

## API Endpoints Reference

### Authentication
| Method | Endpoint | Auth Required | Description |
|--------|----------|---------------|-------------|
| POST | `/api/auth/login` | ❌ | User login, returns JWT token |

### Teams
| Method | Endpoint | Auth Required | Description |
|--------|----------|---------------|-------------|
| GET | `/api/teams` | ✅ | Get all teams |
| GET | `/api/teams/<id>` | ✅ | Get team by ID |
| POST | `/api/teams` | ✅ | Create new team |
| PUT | `/api/teams/<id>` | ✅ | Update team |
| DELETE | `/api/teams/<id>` | ✅ | Delete team |

### Players
| Method | Endpoint | Auth Required | Description |
|--------|----------|---------------|-------------|
| GET | `/api/players` | ✅ | Get all players |
| GET | `/api/players/<id>` | ✅ | Get player by ID |
| POST | `/api/players` | ✅ | Create new player |
| PUT | `/api/players/<id>` | ✅ | Update player |
| DELETE | `/api/players/<id>` | ✅ | Delete player |

### Matches
| Method | Endpoint | Auth Required | Description |
|--------|----------|---------------|-------------|
| GET | `/api/matches` | ✅ | Get all matches |
| GET | `/api/matches/<id>` | ✅ | Get match by ID |
| POST | `/api/matches` | ✅ | Create new match |
| PUT | `/api/matches/<id>` | ✅ | Update match |
| DELETE | `/api/matches/<id>` | ✅ | Delete match |

---

## Limitations & Future Improvements

### Current Limitations

1. **Password Security** ⚠️
   - Passwords stored in **plain text** (not hashed)
   - **Risk**: Database breach exposes all passwords
   - **Academic Note**: Implemented for simplicity; not production-ready

2. **Authorization Granularity**
   - All authenticated users have same permissions
   - No role-based access control (RBAC)
   - No distinction between admin and regular users

3. **Input Validation**
   - Minimal validation on user input
   - No comprehensive data sanitization
   - Vulnerable to malformed data

4. **Error Handling**
   - Basic error responses
   - No detailed logging system
   - Limited error recovery mechanisms

5. **API Rate Limiting**
   - No rate limiting implemented
   - Vulnerable to abuse and DoS attacks

6. **Frontend Architecture**
   - Vanilla JavaScript (no framework)
   - Limited UI/UX features
   - No state management

### Proposed Improvements

#### Security Enhancements
- ✨ **Password Hashing**: Implement bcrypt or argon2 for password storage
- ✨ **Refresh Tokens**: Add refresh token mechanism for extended sessions
- ✨ **HTTPS Enforcement**: Require HTTPS in production
- ✨ **Rate Limiting**: Implement Flask-Limiter for API protection
- ✨ **Input Validation**: Use marshmallow schemas for comprehensive validation
- ✨ **SQL Injection Protection**: Already using ORM, but add query sanitization

#### Feature Additions
- 📊 **Role-Based Access Control**: Admin vs regular user permissions
- 📊 **Player Statistics**: Add goals, assists, cards, etc.
- 📊 **Tournament Brackets**: Knockout stage visualization
- 📊 **Search & Filtering**: Advanced query capabilities
- 📊 **Pagination**: Limit results for large datasets
- 📊 **File Uploads**: Team logos, player photos

#### Technical Improvements
- 🚀 **Caching**: Redis for frequently accessed data
- 🚀 **API Documentation**: Swagger/OpenAPI specification
- 🚀 **Logging**: Structured logging with log levels
- 🚀 **Monitoring**: Health checks and metrics endpoints
- 🚀 **CI/CD Pipeline**: Automated testing and deployment
- 🚀 **Frontend Framework**: Migrate to React or Vue.js
- 🚀 **Database Migrations**: Alembic for schema version control

#### Testing & Quality
- ✅ **Unit Test Coverage**: Achieve >80% code coverage
- ✅ **Integration Tests**: Comprehensive API testing suite
- ✅ **Load Testing**: Performance under concurrent users
- ✅ **Security Audits**: Penetration testing and vulnerability scans

---

## Academic Context

This project demonstrates understanding of:

- **Web Service Architecture**: RESTful API design and implementation
- **Authentication & Authorization**: JWT-based stateless authentication
- **Database Design**: Normalization, relationships, constraints
- **Backend Development**: Python, Flask framework, ORM usage
- **Frontend-Backend Integration**: API consumption, CORS handling
- **Containerization**: Docker for deployment consistency
- **Version Control**: Git workflow and collaboration
- **Security Principles**: Token-based auth, protected endpoints
- **Software Engineering**: Code organization, separation of concerns

---

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/YourFeature`)
3. Commit your changes (`git commit -m 'Add YourFeature'`)
4. Push to the branch (`git push origin feature/YourFeature`)
5. Open a Pull Request

---

## License

This project is open source and available under the [MIT License](LICENSE).

---

## Author

**Mohamed Ayadi**  
GitHub: [@MohamedAyadi19](https://github.com/MohamedAyadi19)

---

## Acknowledgments

- FIFA Arab Cup for inspiration
- Flask documentation and community
- SQLAlchemy for excellent ORM capabilities
- Docker for containerization solutions
