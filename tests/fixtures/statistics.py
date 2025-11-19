from datetime import date, timedelta

import pytest

from app.models.habit import Habit
from app.models.habit_log import HabitLog


@pytest.fixture
def user_with_stats(db, user):
    """Создаёт пользователю 3 привычки и набор логов для тестирования статистики."""
    today = date.today()

    # Привычки
    habits = [
        Habit(name="Habit A", user_id=user.id),
        Habit(name="Habit B", user_id=user.id),
        Habit(name="Habit C", user_id=user.id),
    ]
    db.session.add_all(habits)
    db.session.commit()

    h1, h2, h3 = habits

    # Логи:
    # Habit A → 3/4 выполнено
    h1_logs = [
        (4, True),
        (3, True),
        (2, False),
        (1, True),
    ]

    # Habit B → 0/2 выполнено
    h2_logs = [
        (2, False),
        (1, False),
    ]

    # Habit C → 2/2 выполнено
    h3_logs = [
        (1, True),
        (0, True),
    ]

    logs = []
    for habit, log_data in [
        (h1, h1_logs),
        (h2, h2_logs),
        (h3, h3_logs),
    ]:
        for days_ago, completed in log_data:
            logs.append(
                HabitLog(
                    user_id=user.id,
                    habit_id=habit.id,
                    date=today - timedelta(days=days_ago),
                    completed=completed,
                )
            )

    db.session.add_all(logs)
    db.session.commit()

    return habits
