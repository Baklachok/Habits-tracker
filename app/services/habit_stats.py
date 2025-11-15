from datetime import datetime

from app.models.habit_log import HabitLog


def calculate_streak(logs: list[HabitLog]) -> int:
    """Calculate current streak of completed days."""

    if not logs:
        return 0

    today = datetime.utcnow().date()
    current_date = today

    # храним: {date: completed_bool}
    log_map = {log.date: log.completed for log in logs}

    streak = 0
    while log_map.get(current_date) is True:
        streak += 1
        current_date = current_date.fromordinal(current_date.toordinal() - 1)

    return streak


def calculate_completion_rate(logs: list[HabitLog]) -> float:
    """Calculate completion percentage for all logs."""
    if not logs:
        return 0.0

    completed = sum(1 for log in logs if log.completed)
    total = len(logs)

    return round((completed / total) * 100, 2)
