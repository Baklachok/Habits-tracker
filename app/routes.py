from flask_smorest import Blueprint
from marshmallow import Schema, fields

from app.models import User


# ====== SCHEMAS ======


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    email = fields.Email(required=True)


class CreateUserSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)


# ====== BLUEPRINT ======

user_blp = Blueprint("Users", "users", url_prefix="/api")


# ====== ROUTES ======


@user_blp.route("/users", methods=["GET"])
@user_blp.response(200, UserSchema(many=True))
def get_users():
    """Get all users"""
    users = User.query.all()
    return users
