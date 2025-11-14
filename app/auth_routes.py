from flask import abort
from flask_smorest import Blueprint
from marshmallow import Schema, fields

from app import db
from app.models import User
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
)
import os

auth_blp = Blueprint("Auth", "auth", url_prefix="/auth")

ACCESS_EXPIRES = int(
    os.environ.get("JWT_ACCESS_EXPIRES_SECONDS", 900)
)  # default 15 min


# ====== SCHEMAS ======
class RegisterSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)


class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)


class UserSchema(Schema):
    id = fields.Int()
    email = fields.Email()


# ====== ROUTES ======


@auth_blp.route("/register", methods=["POST"])
@auth_blp.arguments(RegisterSchema)
@auth_blp.response(201, UserSchema)
def register(data):
    email = data["email"]
    password = data["password"]

    if User.query.filter_by(email=email).first():
        abort(400)

    user = User(email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return user


@auth_blp.route("/login", methods=["POST"])
@auth_blp.arguments(LoginSchema)
def login(data):
    email = data["email"]
    password = data["password"]

    user = User.query.filter_by(email=email).first()

    if not user or not user.check_password(password):
        abort(401)

    access = create_access_token(identity=str(user.id))
    refresh = create_refresh_token(identity=str(user.id))

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
    user = User.query.get(int(user_id))
    return user
