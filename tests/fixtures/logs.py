from datetime import date, timedelta

import pytest

from app.models.habit_log import HabitLog


@pytest.fixture()
def habit_logs(user, habit, db):
    """Create multiple habit logs for the user and habit."""
    today = date.today()
    logs = [
        HabitLog(
            user_id=user.id,
            habit_id=habit.id,
            date=today - timedelta(days=4),
            completed=True,
        ),
        HabitLog(
            user_id=user.id,
            habit_id=habit.id,
            date=today - timedelta(days=3),
            completed=True,
        ),
        HabitLog(
            user_id=user.id,
            habit_id=habit.id,
            date=today - timedelta(days=2),
            completed=False,
        ),
        HabitLog(
            user_id=user.id,
            habit_id=habit.id,
            date=today - timedelta(days=1),
            completed=True,
        ),
        HabitLog(user_id=user.id, habit_id=habit.id, date=today, completed=True),
    ]
    db.session.add_all(logs)
    db.session.commit()
    return logs
