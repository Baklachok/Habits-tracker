import logging
from flask_smorest import Blueprint
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.services.habit_stats import get_habit_statistics

logger = logging.getLogger(__name__)

statistics_blp = Blueprint(
    "Statistics",
    "statistics",
    url_prefix="/api/statistics",
    description="Habit statistics endpoints",
)


@statistics_blp.route("/habit/<int:habit_id>")
class HabitStatisticsResource(MethodView):
    @statistics_blp.response(200)
    @jwt_required()
    def get(self, habit_id):
        """Return statistics for a habit"""
        user_id = int(get_jwt_identity())
        logger.info(f"User {user_id} requesting statistics for habit {habit_id}")

        stats = get_habit_statistics(habit_id, user_id)

        logger.info(f"Statistics for habit {habit_id}: {stats}")
        return stats
