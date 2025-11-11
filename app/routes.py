from flask import Blueprint, request, jsonify
from flasgger.utils import swag_from

from .extentions import db
from .models import User

user_bp = Blueprint("users", __name__)


@user_bp.route("/users", methods=["GET"])
@swag_from(
    {
        "tags": ["Users"],
        "summary": "Get all users",
        "responses": {
            200: {
                "description": "List of users",
                "examples": {
                    "application/json": [{"id": 1, "email": "test@example.com"}]
                },
            }
        },
    }
)
def get_users():
    users = User.query.all()
    return jsonify([{"id": u.id, "email": u.email} for u in users])


@user_bp.route("/users", methods=["POST"])
@swag_from(
    {
        "tags": ["Users"],
        "summary": "Create a new user",
        "description": "Создает нового пользователя на основе email и пароля",
        "parameters": [
            {
                "name": "body",
                "in": "body",
                "required": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "email": {"type": "string", "example": "user@example.com"},
                        "password": {"type": "string", "example": "12345"},
                    },
                    "required": ["email", "password"],
                },
            }
        ],
        "responses": {
            201: {"description": "User created successfully"},
            400: {"description": "Bad request"},
        },
    }
)
def create_user():
    data = request.get_json()
    if not data or "email" not in data or "password" not in data:
        return jsonify({"error": "Email and password required"}), 400

    user = User(email=data["email"])
    user.set_password(data["password"])
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User created"}), 201
