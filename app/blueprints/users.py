import logging
from flask_smorest import Blueprint

from app.models.user import User
from app.schemas.user import UserSchema

logger = logging.getLogger(__name__)

# ====== BLUEPRINT ======

user_blp = Blueprint("Users", "users", url_prefix="/api")

# ====== ROUTES ======


@user_blp.route("/users", methods=["GET"])
@user_blp.response(200, UserSchema(many=True))
def get_users():
    """Get all users"""
    logger.info("[GET /api/users] Request received")

    users = User.query.all()

    logger.info(f"[GET /api/users] Retrieved {len(users)} users")
    return users
