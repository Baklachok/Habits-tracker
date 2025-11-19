from datetime import date, timedelta

from app.models.habit import Habit
from app.models.habit_log import HabitLog
from app.services.habit_stats import get_habit_statistics


def test_get_habit_statistics(db, user, habit, habit_logs):
    stats = get_habit_statistics(habit.id, user.id)

    assert stats["total_days"] == 5
    assert stats["completed_days"] == 4
    assert stats["completion_rate"] == 80.0
    assert stats["streak"] == 2  # максимальная серия подряд выполненных дней


def test_habit_with_no_logs(db, user):
    h = Habit(name="Empty Habit", user_id=user.id)
    db.session.add(h)
    db.session.commit()

    stats = get_habit_statistics(h.id, user.id)
    assert stats == {
        "total_days": 0,
        "completed_days": 0,
        "completion_rate": 0.0,
        "streak": 0,
    }


def test_habit_all_completed(db, user):
    h = Habit(name="Perfect Habit", user_id=user.id)
    db.session.add(h)
    db.session.commit()

    today = date.today()
    logs = [
        HabitLog(
            user_id=user.id,
            habit_id=h.id,
            date=today - timedelta(days=i),
            completed=True,
        )
        for i in range(7)
    ]
    db.session.add_all(logs)
    db.session.commit()

    stats = get_habit_statistics(h.id, user.id)
    assert stats["total_days"] == 7
    assert stats["completed_days"] == 7
    assert stats["completion_rate"] == 100.0
    assert stats["streak"] == 7
