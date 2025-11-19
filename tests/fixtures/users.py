import pytest
from flask_jwt_extended import create_access_token

from app.models.user import User


@pytest.fixture()
def user(db):
    """Create and return a test user."""
    u = User(email="test@example.com")
    u.set_password("password")
    db.session.add(u)
    db.session.commit()
    return u


@pytest.fixture()
def user_token(user):
    """Create JWT token for the given user."""
    token = create_access_token(identity=str(user.id))
    return token
