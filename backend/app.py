from flask import Flask, send_from_directory
from flask_cors import CORS
from flasgger import Swagger
from dotenv import load_dotenv
import os

from extensions import db
from services.clean_csv_import import clean_import_from_csv

load_dotenv()

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

    db.init_app(app)
    CORS(app)

    # Swagger Configuration
    swagger_template = {
        "swagger": "2.0",
        "info": {
            "title": "FIFA Arab Cup 2025 API",
            "description": "RESTful API for managing tournament data including teams, players, and matches",
            "version": "1.0.0",
            "contact": {
                "name": "Mohamed Ayadi",
                "email": "ayadimed159@gmail.com"
            }
        },
        "securityDefinitions": {
            "Bearer": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header",
                "description": "JWT Authorization header using the Bearer scheme. Example: 'Bearer {token}'"
            }
        },
        "security": [{"Bearer": []}]
    }

    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": 'apispec',
                "route": '/apispec.json',
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/apidocs/"
    }

    Swagger(app, template=swagger_template, config=swagger_config)

    # IMPORTANT: Register blueprints BEFORE catch-all route
    # This ensures API routes take precedence over frontend
    from routes.matches import matches_bp
    from routes.teams import teams_bp
    from routes.players import players_bp
    from routes.auth import auth_bp
    from routes.leaderboards import leaderboards_bp
    from routes.statistics import statistics_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(players_bp)
    app.register_blueprint(teams_bp)
    app.register_blueprint(leaderboards_bp)
    app.register_blueprint(statistics_bp)
    app.register_blueprint(matches_bp)

    # Serve frontend files (registered LAST so API routes take precedence)
    frontend_folder = os.path.join(os.path.dirname(__file__), 'frontend')
    
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve_frontend(path):
        # Exclude API routes - they are handled by blueprints above
        if path.startswith('api/') or path.startswith('apidocs') or path.startswith('apispec'):
            # Return empty 404 so the routing continues to find blueprint routes
            return '', 404
        if path and os.path.exists(os.path.join(frontend_folder, path)):
            return send_from_directory(frontend_folder, path)
        return send_from_directory(frontend_folder, 'index.html')

    with app.app_context():
        from models import Match, Team
        db.create_all()

        # Auto-import CSV data into the database if empty
        try:
            if Team.query.count() == 0:
                clean_import_from_csv()
        except Exception as exc:
            print(f"⚠️  Auto-import skipped due to error: {exc}")
    
    # Register Flask CLI commands
    @app.cli.command("clean-import")
    def clean_import_command():
        """Clean import: Clear all data and import fresh from CSV (all players per team)"""
        clean_import_from_csv()
        print("✅ Clean import complete!")
    
    @app.cli.command("seed-users")
    def seed_users_command():
        """Seed default users for login"""
        from models import User
        from werkzeug.security import generate_password_hash
        
        # Clear existing users
        User.query.delete()
        
        # Create admin user
        admin = User(
            username='admin',
            password=generate_password_hash('admin123')
        )
        
        # Create test user
        test_user = User(
            username='user',
            password=generate_password_hash('user123')
        )
        
        db.session.add(admin)
        db.session.add(test_user)
        db.session.commit()
        
        print("✅ Users created successfully:")
        print("   admin / admin123")
        print("   user / user123")

    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


