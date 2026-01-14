from flask import Flask, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
import os

from extensions import db

load_dotenv()

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

    db.init_app(app)
    CORS(app)

    from routes.matches import matches_bp
    from routes.teams import teams_bp
    from routes.players import players_bp
    from routes.auth import auth_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(players_bp)
    app.register_blueprint(teams_bp)

    app.register_blueprint(matches_bp)

    # Serve frontend files
    frontend_folder = os.path.join(os.path.dirname(__file__), 'frontend')
    
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve_frontend(path):
        if path and os.path.exists(os.path.join(frontend_folder, path)):
            return send_from_directory(frontend_folder, path)
        return send_from_directory(frontend_folder, 'index.html')

    with app.app_context():
        from models import Match
        db.create_all()

    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


