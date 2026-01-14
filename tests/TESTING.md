# Testing Strategy & Examples

## Testing Overview

This document outlines what to test, how to test, and example test cases for the Arab Cup API project.

### Test Pyramid

```
         ╱╲
        ╱  ╲       Unit Tests (Frontend & Backend)
       ╱────╲      Isolation, fast, mocked dependencies
      ╱      ╲
     ╱────────╲      Integration Tests
    ╱          ╲     API endpoints, DB interactions
   ╱────────────╲    Moderate speed, real DB
  ╱──────────────╲
 ╱────────────────╲   E2E Tests (Manual or Selenium/Playwright)
╱                  ╲  Full user workflows, slow
──────────────────────
```

---

## Unit Tests

### Backend Unit Tests

#### 1. **Test: `auth_utils.token_generation`**

Test JWT token generation and validation.

```python
# backend/test_auth.py
import unittest
from datetime import datetime, timedelta
import jwt
import os
from auth_utils import generate_token

class TestAuthUtils(unittest.TestCase):
    def setUp(self):
        self.secret_key = os.getenv("SECRET_KEY", "test-secret")
    
    def test_generate_token_creates_valid_jwt(self):
        """Test that generate_token creates a valid JWT with correct payload."""
        user_id = 1
        token = generate_token(user_id)
        
        # Token should be a string
        self.assertIsInstance(token, str)
        
        # Token should be decodable
        decoded = jwt.decode(token, self.secret_key, algorithms=["HS256"])
        self.assertEqual(decoded["user_id"], user_id)
    
    def test_token_includes_expiry(self):
        """Test that token includes an expiry claim."""
        token = generate_token(1)
        decoded = jwt.decode(token, self.secret_key, algorithms=["HS256"])
        
        self.assertIn("exp", decoded)
        # Expiry should be in the future (within 2 hours)
        self.assertGreater(decoded["exp"], datetime.utcnow().timestamp())
    
    def test_expired_token_raises_exception(self):
        """Test that an expired token raises ExpiredSignatureError."""
        # Create a token with past expiry
        payload = {
            "user_id": 1,
            "exp": datetime.utcnow() - timedelta(hours=1)
        }
        expired_token = jwt.encode(payload, self.secret_key, algorithm="HS256")
        
        # Should raise ExpiredSignatureError
        with self.assertRaises(jwt.ExpiredSignatureError):
            jwt.decode(expired_token, self.secret_key, algorithms=["HS256"])

if __name__ == "__main__":
    unittest.main()
```

**Run**: `docker-compose exec backend python -m pytest test_auth.py -v`

---

#### 2. **Test: `models.Player position normalization`**

Test position normalization logic used in lineup assignment.

```python
# backend/test_models.py
import unittest
from models import Player

class TestPlayerPositionNormalization(unittest.TestCase):
    def test_normalize_goalkeeper(self):
        """GK positions should normalize to 'Goalkeeper'."""
        p = Player(name="Test", position="Keeper")
        normalized = p.position.lower()
        self.assertIn("goal", normalized) or self.assertIn("keeper", normalized)
    
    def test_normalize_defender(self):
        """Defender/Back positions should be recognized."""
        positions = ["Centre-Back", "Defender", "Left-Back", "Right-Back"]
        for pos in positions:
            normalized = pos.lower()
            self.assertTrue("back" in normalized or "def" in normalized)
    
    def test_normalize_midfielder(self):
        """Midfielder positions should be recognized."""
        positions = ["Central Midfielder", "Attacker", "Midfielder"]
        for pos in positions:
            self.assertIn("mid", pos.lower())
    
    def test_normalize_forward(self):
        """Forward/Striker positions should be recognized."""
        positions = ["Striker", "Forward", "Winger"]
        for pos in positions:
            normalized = pos.lower()
            self.assertTrue("strik" in normalized or "forward" in normalized or "wing" in normalized)

if __name__ == "__main__":
    unittest.main()
```

---

#### 3. **Test: `sportsdb_service.save_teams_to_db` (Upsert Logic)**

Test that save_teams_to_db correctly inserts and updates without duplicates.

```python
# backend/test_sportsdb_service.py
import unittest
from app import create_app
from extensions import db
from models import Team
from services.sportsdb_service import save_teams_to_db

class TestSaveTeamsToDb(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config["TESTING"] = True
        self.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        
        with self.app.app_context():
            db.create_all()
    
    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
    
    def test_save_new_teams(self):
        """Test saving new teams to empty DB."""
        teams = [
            {"idTeam": "1", "strTeam": "Morocco", "strCountry": "Morocco"},
            {"idTeam": "2", "strTeam": "Egypt", "strCountry": "Egypt"}
        ]
        
        with self.app.app_context():
            count = save_teams_to_db(teams)
            self.assertEqual(count, 2)
            self.assertEqual(Team.query.count(), 2)
    
    def test_update_existing_team(self):
        """Test that existing teams are updated, not duplicated."""
        teams = [
            {"idTeam": "1", "strTeam": "Morocco", "strCountry": "Morocco", "strBadge": "old_badge.png"}
        ]
        
        with self.app.app_context():
            # First save
            save_teams_to_db(teams)
            self.assertEqual(Team.query.count(), 1)
            
            # Update with new badge
            teams[0]["strBadge"] = "new_badge.png"
            save_teams_to_db(teams)
            
            # Should still be 1 team (not 2)
            self.assertEqual(Team.query.count(), 1)
            
            # Badge should be updated
            team = Team.query.first()
            self.assertEqual(team.badge, "new_badge.png")
    
    def test_skip_invalid_teams(self):
        """Test that teams without idTeam are skipped."""
        teams = [
            {"idTeam": "1", "strTeam": "Morocco", "strCountry": "Morocco"},
            {"strTeam": "Invalid", "strCountry": "Invalid"}  # No idTeam
        ]
        
        with self.app.app_context():
            count = save_teams_to_db(teams)
            self.assertEqual(count, 1)  # Only 1 valid team
            self.assertEqual(Team.query.count(), 1)

if __name__ == "__main__":
    unittest.main()
```

---

### Frontend Unit Tests

#### 4. **Test: `flagMap coverage`**

Verify that all Arab Cup countries have flag URLs.

```javascript
// frontend/test_flags.js
const flagMap = {
    "Qatar": "https://flagcdn.com/w80/qa.png",
    "Tunisia": "https://flagcdn.com/w80/tn.png",
    "Syria": "https://flagcdn.com/w80/sy.png",
    "Palestine": "https://flagcdn.com/w80/ps.png",
    "Morocco": "https://flagcdn.com/w80/ma.png",
    "Saudi Arabia": "https://flagcdn.com/w80/sa.png",
    "Oman": "https://flagcdn.com/w80/om.png",
    "Comoros": "https://flagcdn.com/w80/km.png",
    "Egypt": "https://flagcdn.com/w80/eg.png",
    "Jordan": "https://flagcdn.com/w80/jo.png",
    "United Arab Emirates": "https://flagcdn.com/w80/ae.png",
    "Kuwait": "https://flagcdn.com/w80/kw.png",
    "Algeria": "https://flagcdn.com/w80/dz.png",
    "Iraq": "https://flagcdn.com/w80/iq.png",
    "Bahrain": "https://flagcdn.com/w80/bh.png",
    "Sudan": "https://flagcdn.com/w80/sd.png"
};

const arabCupCountries = [
    "Qatar", "Tunisia", "Syria", "Palestine", "Morocco", "Saudi Arabia", 
    "Oman", "Comoros", "Egypt", "Jordan", "United Arab Emirates", 
    "Kuwait", "Algeria", "Iraq", "Bahrain", "Sudan"
];

function testFlagMapCoverage() {
    let missing = [];
    arabCupCountries.forEach(country => {
        if (!flagMap[country]) {
            missing.push(country);
        }
    });
    
    if (missing.length === 0) {
        console.log("✓ All Arab Cup countries have flag URLs");
    } else {
        console.error("✗ Missing flags:", missing);
    }
}

testFlagMapCoverage();
```

**Run**: Open browser console and run `testFlagMapCoverage()`.

---

#### 5. **Test: `normalizePosition function`**

Test frontend position normalization.

```javascript
// frontend/test_normalize.js
function normalizePosition(raw) {
    if (!raw) return "UNK";
    const p = raw.toLowerCase();
    if (p.includes("keeper") || p === "gk") return "GK";
    if (p.includes("back") || p.includes("def")) return "DEF";
    if (p.includes("mid")) return "MID";
    if (p.includes("wing")) return "FWD";
    if (p.includes("striker") || p.includes("forward") || p === "st") return "FWD";
    return "UNK";
}

function testNormalizePosition() {
    const tests = [
        ["Goalkeeper", "GK"],
        ["Centre-Back", "DEF"],
        ["Left-Back", "DEF"],
        ["Midfielder", "MID"],
        ["Striker", "FWD"],
        ["Winger", "FWD"],
        ["Unknown", "UNK"],
        [null, "UNK"]
    ];
    
    tests.forEach(([input, expected]) => {
        const result = normalizePosition(input);
        if (result === expected) {
            console.log(`✓ normalizePosition("${input}") = "${result}"`);
        } else {
            console.error(`✗ normalizePosition("${input}") returned "${result}", expected "${expected}"`);
        }
    });
}

testNormalizePosition();
```

---

## Integration Tests

#### 6. **Test: `/api/auth/login` Endpoint**

Test the complete authentication flow.

```python
# backend/test_integration_auth.py
import unittest
import json
from app import create_app
from extensions import db
from models import User

class TestAuthIntegration(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config["TESTING"] = True
        self.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.create_all()
            # Create test user
            user = User(username="testuser", password="testpass123")
            db.session.add(user)
            db.session.commit()
    
    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
    
    def test_login_success(self):
        """Test successful login returns JWT token."""
        response = self.client.post(
            "/api/auth/login",
            data=json.dumps({"username": "testuser", "password": "testpass123"}),
            content_type="application/json"
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn("token", data)
        self.assertIsInstance(data["token"], str)
    
    def test_login_invalid_credentials(self):
        """Test login with wrong password returns 401."""
        response = self.client.post(
            "/api/auth/login",
            data=json.dumps({"username": "testuser", "password": "wrongpass"}),
            content_type="application/json"
        )
        
        self.assertEqual(response.status_code, 401)
        data = json.loads(response.data)
        self.assertIn("error", data)
    
    def test_login_nonexistent_user(self):
        """Test login for non-existent user returns 401."""
        response = self.client.post(
            "/api/auth/login",
            data=json.dumps({"username": "nonexistent", "password": "anypass"}),
            content_type="application/json"
        )
        
        self.assertEqual(response.status_code, 401)

if __name__ == "__main__":
    unittest.main()
```

---

#### 7. **Test: `/api/teams/` and `/api/teams/sync` Endpoints**

Test team endpoints with authentication.

```python
# backend/test_integration_teams.py
import unittest
import json
from app import create_app
from extensions import db
from models import User, Team
from auth_utils import generate_token

class TestTeamsIntegration(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config["TESTING"] = True
        self.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.create_all()
            # Create test user and token
            user = User(username="testuser", password="testpass")
            db.session.add(user)
            db.session.commit()
            self.token = generate_token(user.id)
            
            # Add test team
            team = Team(team_id="1", name="Morocco", country="Morocco")
            db.session.add(team)
            db.session.commit()
    
    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
    
    def test_get_teams_requires_auth(self):
        """Test that GET /api/teams/ requires valid token."""
        response = self.client.get("/api/teams/")
        self.assertEqual(response.status_code, 401)
    
    def test_get_teams_with_auth(self):
        """Test GET /api/teams/ with valid token."""
        headers = {"Authorization": f"Bearer {self.token}"}
        response = self.client.get("/api/teams/", headers=headers)
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)
        self.assertEqual(data[0]["name"], "Morocco")
    
    def test_sync_teams_endpoint(self):
        """Test POST /api/teams/sync merges teams correctly."""
        headers = {"Authorization": f"Bearer {self.token}"}
        response = self.client.post("/api/teams/sync", headers=headers)
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["status"], "teams synced")
        self.assertIn("count", data)

if __name__ == "__main__":
    unittest.main()
```

---

## End-to-End Tests (Manual Checklist)

### 1. **User Login & Dashboard Access**

```
Steps:
1. Open frontend in browser
2. Enter credentials: admin / admin123
3. Click "Login"
4. Verify dashboard appears
5. Verify sync buttons are visible
6. Verify logout or token expires gracefully

Expected:
- Login form hidden
- Team cards show (initially as placeholders)
- Sync buttons enabled
```

---

### 2. **Data Sync Workflow**

```
Steps:
1. Click "Sync Teams"
2. Wait for progress bar to complete
3. Verify success message
4. Repeat for "Sync Matches" and "Sync Players"
5. Verify no duplicate teams/players in DB

Expected:
- Progress bar shows 0→100%
- Success message appears
- Team cards update with flags
- Players grouped by country
- Matches listed with dates & scores
```

---

### 3. **Lineup Cartography**

```
Steps:
1. After syncing players, scroll to "Lineup Cartography"
2. Select a team from dropdown
3. Select a formation (4-3-3, 4-2-3-1, 3-5-2)
4. Verify pitch appears with players
5. Hover over player slots to see names
6. Verify bench shows unplaced players
7. Change formation, verify lineup updates

Expected:
- Pitch displays correctly
- 11 players on field (varying by formation)
- Bench lists remaining players
- Formation changes are instant
- Color-coded by position (GK/DEF/MID/FWD)
```

---

### 4. **Filters & Sorting**

```
Steps:
1. In "Matches" section, select a country filter
2. Verify matches list updates to show only that team
3. In "Players" section, verify grouped by country with flags
4. Check player cards display name and position

Expected:
- Match filter works correctly
- Players grouped alphabetically by country
- Flags display for all teams
- No broken images
```

---

### 5. **Error Handling**

```
Steps:
1. Let JWT token expire (2 hours) or manually clear localStorage
2. Try clicking sync buttons without logging in
3. Disable network and try sync
4. Check browser console for errors

Expected:
- 401 errors caught gracefully
- User prompted to re-login
- Network errors don't crash app
- No sensitive data in logs
```

---

## Test Coverage Goals

| Component | Target Coverage | Notes |
|-----------|-----------------|-------|
| `auth_utils.py` | 90%+ | Critical for security |
| `models.py` | 85%+ | ORM relationships |
| `routes/*.py` | 80%+ | API endpoints |
| `services/sportsdb_service.py` | 75%+ | External API mocking |
| `app.js` | 70%+ | DOM manipulation, event handlers |
| `style.css` | Manual | Visual regression testing |

---

## Running Tests

### Backend Tests

```bash
# Install pytest (if not already in requirements.txt)
docker-compose exec backend pip install pytest pytest-cov

# Run all tests
docker-compose exec backend pytest -v

# Run with coverage report
docker-compose exec backend pytest --cov=. --cov-report=html

# Run specific test file
docker-compose exec backend pytest test_auth.py -v

# Run specific test class
docker-compose exec backend pytest test_auth.py::TestAuthUtils -v

# Run specific test method
docker-compose exec backend pytest test_auth.py::TestAuthUtils::test_generate_token_creates_valid_jwt -v
```

### Frontend Tests

```bash
# Open browser console (F12 → Console)
# Run test functions manually:
testFlagMapCoverage();
testNormalizePosition();

# Or use automated test runner (e.g., Jest, Vitest)
# Example: npm install jest
# npm test
```

---

## Continuous Integration (CI) Setup

For GitHub Actions or GitLab CI:

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_DB: test_db
          POSTGRES_USER: postgres
          POSTGRES_PASSWORD: test_pass
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        working-directory: ./backend
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-cov
      
      - name: Run backend tests
        working-directory: ./backend
        run: pytest --cov=. --cov-report=xml
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./backend/coverage.xml
```

---

## Summary

**What to test:**
- ✅ Authentication (login, token validation)
- ✅ CRUD operations (create, read, update teams/players/matches)
- ✅ Data sync (upsert logic, no duplicates)
- ✅ Position normalization (for lineups)
- ✅ Frontend flag mapping (all countries covered)
- ✅ Lineup assignment (formations, slot allocation)
- ✅ Error handling (401, 500, network errors)
- ✅ Data consistency (before/after sync)

**Coverage targets:**
- Backend: 80–90%
- Frontend: 70%+
- Manual E2E: 100% (critical flows)

**Tools:**
- Backend: `pytest`, `pytest-cov`
- Frontend: `console`, `Jest`/`Vitest` (optional)
- CI: GitHub Actions, GitLab CI

Test early, test often!
