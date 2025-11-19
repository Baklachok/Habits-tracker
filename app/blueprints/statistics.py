import logging

from flask import jsonify
from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.services.habit_stats import get_habit_statistics
from app.services.user_stats import (
    fetch_user_habits,
    build_empty_stats,
    fetch_logs_for_habits,
    logs_to_dataframe,
    calculate_habit_stats,
    select_top_habits,
)

logger = logging.getLogger(__name__)

statistics_blp = Blueprint(
    "Statistics",
    "statistics",
    url_prefix="/api/statistics",
    description="Habit statistics endpoints",
)


# ----------------------------------------------------------------------
# Habit statistics (per one habit)
# ----------------------------------------------------------------------
@statistics_blp.route("/habit/<int:habit_id>")
class HabitStatisticsResource(MethodView):
    @statistics_blp.response(200)
    @jwt_required()
    def get(self, habit_id):
        """Return statistics for a single habit."""
        user_id = int(get_jwt_identity())
        logger.info(f"[GET] Habit statistics: user={user_id}, habit={habit_id}")

        stats = get_habit_statistics(habit_id, user_id)

        logger.info(f"[OK] Habit {habit_id} statistics: {stats}")
        return stats


# ----------------------------------------------------------------------
# User statistics (all habits)
# ----------------------------------------------------------------------


@statistics_blp.get("/user/<int:user_id>")
@jwt_required()
def user_statistics(user_id: int):
    """Return aggregated statistics for all user habits."""
    logger.info(f"[GET] User statistics: user={user_id}")

    # 1. Fetch habits
    habits = fetch_user_habits(user_id)
    if not habits:
        return jsonify(build_empty_stats()), 200

    habit_ids = [h.id for h in habits]

    # 2. Fetch logs
    logs = fetch_logs_for_habits(habit_ids)
    if not logs:
        return jsonify(build_empty_stats(total_habits=len(habits))), 200

    # 3. DataFrame processing
    df = logs_to_dataframe(logs)
    stats = calculate_habit_stats(df)

    # 4. Average completion rate
    avg_rate = round(stats["completion_rate"].mean(), 2)

    # 5. Top habits
    top_habits = select_top_habits(stats, habits)

    response = {
        "total_habits": len(habits),
        "average_completion_rate": avg_rate,
        "top_habits": top_habits,
    }

    logger.info(f"[OK] User statistics ready: user={user_id}, stats={response}")
    return jsonify(response), 200
