from app import create_app
from extensions import db
from models import Match, Team, Player, User, db

app = create_app()

with app.app_context():
    db.create_all()
    print("Database tables created successfully.")

with app.app_context():
    db.create_all()

    if not User.query.filter_by(username="admin").first():
        admin = User(username="admin", password="admin123")
        db.session.add(admin)
        db.session.commit()

    print("Database initialized")