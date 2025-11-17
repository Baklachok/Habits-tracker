import logging
from datetime import datetime
from app.models.habit_log import HabitLog

logger = logging.getLogger(__name__)


def calculate_streak(logs: list[HabitLog]) -> int:
    """Calculate current streak of completed days."""

    logger.info("calculate_streak started: logs_count=%s", len(logs))

    if not logs:
        logger.info("No logs provided → streak = 0")
        return 0

    today = datetime.utcnow().date()
    current_date = today

    # храним {date: completed_bool}
    log_map = {log.date: log.completed for log in logs}
    logger.debug("log_map generated: %s", log_map)

    streak = 0
    while log_map.get(current_date) is True:
        streak += 1
        logger.debug("Streak +1 for date=%s (streak=%s)", current_date, streak)

        # переходим на предыдущий день
        current_date = current_date.fromordinal(current_date.toordinal() - 1)

    logger.info("calculate_streak finished: streak=%s", streak)
    return streak


def calculate_completion_rate(logs: list[HabitLog]) -> float:
    """Calculate completion percentage for all logs."""
    logger.info("calculate_completion_rate started: logs_count=%s", len(logs))

    if not logs:
        logger.info("No logs provided → completion_rate = 0.0")
        return 0.0

    completed = sum(1 for log in logs if log.completed)
    total = len(logs)

    completion_rate = round((completed / total) * 100, 2)

    logger.info(
        "calculate_completion_rate finished: completed=%s, total=%s, rate=%s%%",
        completed,
        total,
        completion_rate,
    )

    return completion_rate


def compute_habit_stats(habit_id: int, user_id: int) -> dict:
    """Compute full statistics for a habit."""

    logs: list[HabitLog] = (
        HabitLog.query.filter_by(habit_id=habit_id, user_id=user_id)
        .order_by(HabitLog.date.asc())
        .all()
    )

    logger.debug(
        "[habit_stats_service] Loaded %s logs for habit=%s user=%s",
        len(logs),
        habit_id,
        user_id,
    )

    streak = calculate_streak(logs)
    completion_rate = calculate_completion_rate(logs)

    logger.info(
        "[habit_stats_service] Computed stats for habit=%s user=%s: streak=%s, completion_rate=%s",
        habit_id,
        user_id,
        streak,
        completion_rate,
    )

    return {
        "habit_id": habit_id,
        "streak": streak,
        "completion_rate": completion_rate,
    }
