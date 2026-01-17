from flask import Blueprint, request, jsonify
from models import User
from extensions import db
from auth_utils import generate_token
from werkzeug.security import check_password_hash

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")

@auth_bp.route("/login", methods=["POST"])
def login():
    """
    User Login - Authenticate and receive JWT token
    ---
    tags:
      - Authentication
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - username
            - password
          properties:
            username:
              type: string
              example: admin
            password:
              type: string
              example: admin123
    responses:
      200:
        description: Login successful, JWT token returned
        schema:
          type: object
          properties:
            token:
              type: string
              example: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
      401:
        description: Invalid credentials
        schema:
          type: object
          properties:
            error:
              type: string
              example: Invalid credentials
    """
    data = request.json

    user = User.query.filter_by(username=data.get("username")).first()

    if not user or not check_password_hash(user.password, data.get("password")):
        return jsonify({"error": "Invalid credentials"}), 401

    token = generate_token(user.id)
    return jsonify({"token": token})
