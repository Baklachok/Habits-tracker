import pandas as pd
from datetime import timedelta
from app.models.habit_log import HabitLog
from app import db


def get_habit_statistics(habit_id: int, user_id: int) -> dict:
    """
    Возвращает статистику по привычке:
    total_days, completed_days, completion_rate, streak
    """

    logs = (
        db.session.query(HabitLog)
        .filter_by(habit_id=habit_id, user_id=user_id)
        .order_by(HabitLog.date.asc())
        .all()
    )

    if not logs:
        return {
            "total_days": 0,
            "completed_days": 0,
            "completion_rate": 0.0,
            "streak": 0,
        }

    df = pd.DataFrame([{"date": log.date, "completed": log.completed} for log in logs])
    df.sort_values("date", inplace=True)
    df["completed"] = df["completed"].astype(int)

    total_days = len(df)
    completed_days = df["completed"].sum()
    completion_rate = round(completed_days / total_days * 100, 2)

    # Рассчитываем максимальную серию подряд выполненных дней
    df["gap"] = (df["date"] - df["date"].shift(1)).fillna(pd.Timedelta(days=1))
    df["new_streak"] = (df["gap"] != timedelta(days=1)) | (df["completed"] == 0)
    df["streak_group"] = df["new_streak"].cumsum()
    streaks = df[df["completed"] == 1].groupby("streak_group").size()
    max_streak = int(streaks.max()) if not streaks.empty else 0

    # Приводим к чистым Python типам
    return {
        "total_days": int(total_days),
        "completed_days": int(completed_days),
        "completion_rate": float(completion_rate),
        "streak": int(max_streak),
    }
