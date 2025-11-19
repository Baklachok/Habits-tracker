import pytest

from app.models.habit import Habit


@pytest.fixture()
def habit(user, db):
    """Create and return a test habit for the user."""
    h = Habit(name="Test Habit", user_id=user.id)
    db.session.add(h)
    db.session.commit()
    return h
