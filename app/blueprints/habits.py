import logging
from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity

from app import db
from app.models.habit import Habit
from app.schemas.habit import HabitSchema, HabitCreateSchema, HabitQuerySchema
from app.schemas.habit_stats import HabitStatsSchema
from app.services.habit_stats import compute_habit_stats

logger = logging.getLogger(__name__)

habit_blp = Blueprint("habits", __name__, description="CRUD operations for habits")


def _get_current_user_id() -> int:
    return int(get_jwt_identity())


def _get_user_habit_or_404(habit_id: int, user_id: int) -> Habit:
    """Возвращает привычку пользователя или 404."""
    return Habit.query.filter_by(id=habit_id, user_id=user_id).first_or_404()


@habit_blp.route("/")
class HabitListResource(MethodView):
    @habit_blp.arguments(HabitQuerySchema, location="query")
    @habit_blp.response(200, HabitSchema(many=True))
    @jwt_required()
    def get(self, query_params):
        """Get all habits for current user."""
        user_id = _get_current_user_id()
        logger.info("[GET /habits] user=%s filters=%s", user_id, query_params)

        habits_query = Habit.query.filter_by(user_id=user_id)

        frequency = query_params.get("frequency")
        if frequency:
            logger.debug("Filtering by frequency=%s", frequency)
            habits_query = habits_query.filter_by(frequency=frequency)

        habits = habits_query.all()
        logger.info("[GET /habits] user=%s returned=%s habits", user_id, len(habits))

        return habits

    @habit_blp.arguments(HabitCreateSchema)
    @habit_blp.response(201, HabitSchema)
    @jwt_required()
    def post(self, new_data):
        """Create a new habit."""
        user_id = _get_current_user_id()
        logger.info("[POST /habits] user=%s payload=%s", user_id, new_data)

        habit = Habit(user_id=user_id, **new_data)
        db.session.add(habit)
        db.session.commit()

        logger.info("[POST /habits] habit created id=%s", habit.id)
        return habit


@habit_blp.route("/<int:habit_id>")
class HabitResource(MethodView):
    @habit_blp.response(200, HabitSchema)
    @jwt_required()
    def get(self, habit_id):
        """Get habit by id."""
        user_id = _get_current_user_id()
        logger.info("[GET /habits/%s] user=%s", habit_id, user_id)

        habit = _get_user_habit_or_404(habit_id, user_id)

        logger.info("[GET /habits/%s] success", habit_id)
        return habit

    @habit_blp.arguments(HabitCreateSchema)
    @habit_blp.response(200, HabitSchema)
    @jwt_required()
    def patch(self, update_data, habit_id):
        """Update habit by id."""
        user_id = _get_current_user_id()
        logger.info(
            "[PATCH /habits/%s] user=%s update=%s",
            habit_id,
            user_id,
            update_data,
        )

        habit = _get_user_habit_or_404(habit_id, user_id)

        for key, value in update_data.items():
            logger.debug("Updating %s=%s", key, value)
            setattr(habit, key, value)

        db.session.commit()
        logger.info("[PATCH /habits/%s] updated", habit_id)

        return habit

    @habit_blp.response(204)
    @jwt_required()
    def delete(self, habit_id):
        """Delete habit by id."""
        user_id = _get_current_user_id()
        logger.warning("[DELETE /habits/%s] user=%s", habit_id, user_id)

        habit = _get_user_habit_or_404(habit_id, user_id)

        db.session.delete(habit)
        db.session.commit()

        logger.info("[DELETE /habits/%s] deleted", habit_id)
        return "", 204


@habit_blp.route("/<int:habit_id>/stats")
class HabitStatsResource(MethodView):
    @habit_blp.response(200, HabitStatsSchema)
    @jwt_required()
    def get(self, habit_id):
        """Return progress statistics for a habit."""
        user_id = _get_current_user_id()

        logger.info("[GET /habits/%s/stats] user=%s", habit_id, user_id)

        # Проверяем, что привычка принадлежит пользователю
        _get_user_habit_or_404(habit_id, user_id)

        # Статистика полностью в сервисе
        stats = compute_habit_stats(habit_id, user_id)

        logger.info("[GET /habits/%s/stats] stats=%s", habit_id, stats)

        return stats
