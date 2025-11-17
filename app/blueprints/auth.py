import logging
import os
from flask import abort
from flask_smorest import Blueprint
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
)

from app import db
from app.models.user import User
from app.schemas.user import RegisterSchema, UserSchema, LoginSchema

logger = logging.getLogger(__name__)

auth_blp = Blueprint("Auth", "auth", url_prefix="/auth")

ACCESS_EXPIRES = int(os.environ.get("JWT_ACCESS_EXPIRES_SECONDS", 900))


@auth_blp.route("/register", methods=["POST"])
@auth_blp.arguments(RegisterSchema)
@auth_blp.response(201, UserSchema)
def register(data):
    email = data["email"]
    password = data["password"]

    logger.info("Attempting to register user: email=%s", email)

    if User.query.filter_by(email=email).first():
        logger.warning("Registration failed: email already exists: %s", email)
        abort(400)

    user = User(email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    logger.info("User registered successfully: user_id=%s, email=%s", user.id, email)

    return user


@auth_blp.route("/login", methods=["POST"])
@auth_blp.arguments(LoginSchema)
def login(data):
    email = data["email"]
    password = data["password"]

    logger.info("Login attempt: email=%s", email)

    user = User.query.filter_by(email=email).first()

    if not user:
        logger.warning("Login failed: user not found: email=%s", email)
        abort(401)

    if not user.check_password(password):
        logger.warning("Login failed: incorrect password for email=%s", email)
        abort(401)

    access = create_access_token(identity=str(user.id))
    refresh = create_refresh_token(identity=str(user.id))

    logger.info("Login successful: user_id=%s", user.id)

    return {
        "access_token": access,
        "refresh_token": refresh,
        "user": UserSchema().dump(user),
    }


@auth_blp.route("/me", methods=["GET"])
@auth_blp.response(200, UserSchema)
@jwt_required()
@auth_blp.doc(security=[{"BearerAuth": []}])
def me():
    user_id = get_jwt_identity()
    logger.info("Fetching /me for user_id=%s", user_id)

    user = User.query.get(int(user_id))

    if not user:
        logger.error("User not found in /me: user_id=%s", user_id)
        abort(404)

    logger.debug("Successfully returned /me for user_id=%s", user_id)

    return user
