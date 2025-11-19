import pandas as pd

from app.models.habit import Habit
from app.models.habit_log import HabitLog


def build_empty_stats(total_habits: int = 0):
    """Returns an empty statistics response."""
    return {
        "total_habits": total_habits,
        "average_completion_rate": 0,
        "top_habits": [],
    }


def fetch_user_habits(user_id: int):
    """Fetch all habits of a user."""
    return Habit.query.filter_by(user_id=user_id).all()


def fetch_logs_for_habits(habit_ids: list[int]):
    """Fetch all logs for a list of habit IDs."""
    return HabitLog.query.filter(HabitLog.habit_id.in_(habit_ids)).all()


def logs_to_dataframe(logs: list[HabitLog]) -> pd.DataFrame:
    """Convert HabitLog objects to a Pandas DataFrame."""
    return pd.DataFrame(
        {
            "habit_id": [log.habit_id for log in logs],
            "completed": [log.completed for log in logs],
        }
    )


def calculate_habit_stats(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate stats per habit: total days, completed days, completion rate."""
    stats = (
        df.groupby("habit_id")
        .agg(
            total_days=("completed", "count"),
            completed_days=("completed", "sum"),
        )
        .reset_index()
    )
    stats["completion_rate"] = stats["completed_days"] / stats["total_days"] * 100
    return stats


def select_top_habits(stats: pd.DataFrame, habits: list[Habit], limit: int = 3):
    """Return top N habits by completed days, enriched with habit names."""
    habit_names = {h.id: h.name for h in habits}

    top = (
        stats.sort_values("completed_days", ascending=False)
        .head(limit)
        .to_dict(orient="records")
    )

    for item in top:
        item["name"] = habit_names[item["habit_id"]]

    return top
