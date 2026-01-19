# FIFA Arab Cup 2025 - Football Analytics Platform

A full-stack web application delivering football team statistics, player insights, and match analytics through a normalized PostgreSQL database, Flask REST API, and responsive JavaScript frontend.

---

## 🎯 Purpose & Objectives

### Purpose
Centralize FIFA Arab Cup tournament data into a consistent, queryable platform that eliminates inconsistent naming conventions and manual data cleaning. This project demonstrates practical application of web services, database design, and REST API development for academic coursework at Tunis Business School.

### Key Objectives
1. **Data Normalization** - Transform raw CSV data into a normalized relational database (3NF)
2. **REST API Development** - Build a secure, scalable API following REST principles
3. **Authentication & Security** - Implement JWT-based authentication for protected resources
4. **Automated Data Pipeline** - Create reproducible CSV-to-database import workflows
5. **Interactive Frontend** - Develop a responsive web interface for data visualization
6. **Containerization** - Deploy using Docker for consistency across environments

### Academic Learning Goals
- Master REST API design patterns and HTTP methods
- Understand relational database modeling and normalization
- Implement service layer architecture and separation of concerns
- Practice secure authentication and authorization
- Apply data engineering principles for reproducible pipelines

---

## 🚀 How to Run

### Prerequisites
- Python 3.8 or higher
- Docker & Docker Compose (recommended for production-like setup)
- Git

---

### Option 1: Docker Setup (Recommended)

**Step 1: Clone the repository**
```bash
git clone https://github.com/MohamedAyadi19/FIFA-Arab-Cup-Project.git
cd updated_arab_cup
```

**Step 2: Create environment file**
```bash
# Windows (PowerShell)
@"
SECRET_KEY=your_secret_key_minimum_32_characters_long
DATABASE_URL=postgresql://postgres:postgres@db:5432/arab_cup
FLASK_ENV=development
"@ | Out-File -FilePath .env -Encoding utf8

# Windows (Command Prompt)
echo SECRET_KEY=your_secret_key_minimum_32_characters_long > .env
echo DATABASE_URL=postgresql://postgres:postgres@db:5432/arab_cup >> .env
echo FLASK_ENV=development >> .env
```

**Step 3: Start services**
```bash
docker-compose up --build
```

**Step 4: Initialize database (in a new terminal)**
```bash
# Wait 10 seconds for PostgreSQL to start
docker-compose exec backend python init_db.py
docker-compose exec backend python import_data.py
```

**Step 5: Access application**
- Open browser to `http://localhost:5000`
- Default login credentials:
  - Username: `admin`
  - Password: `admin123`

---

### Option 2: Local Development Setup

**Step 1: Clone the repository**
```bash
git clone https://github.com/MohamedAyadi19/FIFA-Arab-Cup-Project.git
cd updated_arab_cup
```

**Step 2: Create virtual environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

**Step 3: Install dependencies**
```bash
cd backend
pip install -r requirements.txt
```

**Step 4: Configure environment variables**
```bash
# Windows (PowerShell)
$env:SECRET_KEY="your_secret_key_minimum_32_characters_long"
$env:DATABASE_URL="sqlite:///arab_cup.db"
$env:FLASK_ENV="development"

# Windows (Command Prompt)
set SECRET_KEY=your_secret_key_minimum_32_characters_long
set DATABASE_URL=sqlite:///arab_cup.db
set FLASK_ENV=development
```

**Step 5: Initialize database and import data**
```bash
python init_db.py
python import_data.py
```

**Step 6: Run the application**
```bash
python app.py
```

**Step 7: Access application**
- Open browser to `http://localhost:5000`
- Default login credentials:
  - Username: `admin`
  - Password: `admin123`

---


**Import data fails:**
- Verify CSV files are present: `teams.csv`, `players.csv`, `matches.csv`
- Check file encoding is UTF-8
- Review import logs for specific error messages

---

## ✨ Features

- 🏆 **Team Dashboards** - Interactive cards with W-D-L records, goals, and performance metrics
- 👤 **Player Search** - Real-time search with autocomplete and detailed profiles
- ⚽ **Match History** - Complete fixture lists with scores, dates, and venues
- 📊 **Leaderboards** - Rankings for top scorers, assists, defenders, and standings
- 🔐 **JWT Authentication** - Secure token-based authentication for admin workflows
- 📈 **Statistics API** - Team and player aggregates exposed via REST endpoints
- 🐳 **Docker Deployment** - Containerized PostgreSQL and Flask services
- 🔄 **Deterministic Import** - Reproducible CSV-to-database pipeline

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| **Backend** | Flask 3.x, Python, SQLAlchemy ORM |
| **Database** | PostgreSQL 15 (Docker), SQLite (dev) |
| **Frontend** | HTML5, CSS3, Vanilla JavaScript, Fetch API |
| **Auth** | JWT (Flask-JWT-Extended) |
| **Data Processing** | pandas (CSV import) |
| **DevOps** | Docker, Docker Compose |

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────┐
│         PRESENTATION LAYER               │
│  HTML/CSS/JavaScript                     │
│  - Team Cards  - Player Search           │
│  - Match Tables - Leaderboards           │
└──────────────┬──────────────────────────┘
               │ HTTP/JSON
               ▼
┌─────────────────────────────────────────┐
│        APPLICATION LAYER                 │
│  Flask REST API (Blueprints)             │
│  - /api/auth      - /api/teams           │
│  - /api/players   - /api/matches         │
│  - /api/statistics - /api/leaderboards   │
│                                          │
│  Service Layer                           │
│  - Normalization  - Aggregation          │
│  - Query Logic    - Data Mapping         │
└──────────────┬──────────────────────────┘
               │ SQL Queries
               ▼
┌─────────────────────────────────────────┐
│           DATA LAYER                     │
│  PostgreSQL (Normalized Schema)          │
│  Tables: users, teams, players, matches, │
│          team_statistics, player_stats   │
└─────────────────────────────────────────┘
```

---



---

## 📁 Project Structure

```
.
├── backend/
│   ├── app.py                  # Flask application factory
│   ├── models.py               # SQLAlchemy models
│   ├── extensions.py           # Flask extensions
│   ├── auth_utils.py           # JWT utilities
│   ├── init_db.py              # Database initialization
│   ├── import_data.py          # CSV import pipeline
│   ├── requirements.txt        # Python dependencies
│   ├── routes/                 # API endpoint blueprints
│   │   ├── auth.py
│   │   ├── teams.py
│   │   ├── players.py
│   │   ├── matches.py
│   │   ├── statistics.py
│   │   └── leaderboards.py
│   └── services/
│       └── db_data_service.py  # Data access layer
├── frontend/
│   ├── index.html              # Main page
│   ├── app.js                  # Frontend logic
│   ├── statistics.js           # Stats dashboard
│   └── style.css               # Styling
├── data/                       # CSV datasets
│   ├── teams.csv
│   ├── players.csv
│   └── matches.csv
├── tests/
│   └── TESTING.md              # Test documentation
├── docker-compose.yml          # Container orchestration
└── .env                        # Environment variables
```

---

## 📊 Results & Performance

### Achievements

- ✅ Relational database with 6 normalized tables
- ✅ RESTful API with 15+ endpoints
- ✅ Responsive frontend with 4 core features
- ✅ Deterministic CSV pipeline (100% reproducible)
- ✅ Zero data inconsistencies
- ✅ Sub-500ms query response times
- ✅ Mobile-responsive design
- ✅ JWT authentication with 2-hour token TTL

---

# 👨‍💻 Author

**Mohamed Ayadi**  
📧 ayadimed159@gmail.com  
🎓 Tunis Business School  
💼 GitHub: [@MohamedAyadi19](https://github.com/MohamedAyadi19)

---

## 📄 License

This project is open source and available under the MIT License.

---
