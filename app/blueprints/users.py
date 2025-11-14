from flask_smorest import Blueprint

from app.models.user import User
from app.schemas.user import UserSchema

# ====== BLUEPRINT ======

user_blp = Blueprint("Users", "users", url_prefix="/api")


# ====== ROUTES ======


@user_blp.route("/users", methods=["GET"])
@user_blp.response(200, UserSchema(many=True))
def get_users():
    """Get all users"""
    users = User.query.all()
    return users
