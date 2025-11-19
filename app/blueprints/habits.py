import logging
from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required

from app import db
from app.models.habit import Habit
from app.schemas.habit import HabitSchema, HabitCreateSchema, HabitQuerySchema
from app.utils.habit_helpers import get_current_user_id, get_user_habit_or_404

logger = logging.getLogger(__name__)

habit_blp = Blueprint("habits", __name__, description="CRUD operations for habits")


@habit_blp.route("/")
class HabitListResource(MethodView):
    @habit_blp.arguments(HabitQuerySchema, location="query")
    @habit_blp.response(200, HabitSchema(many=True))
    @jwt_required()
    def get(self, query_params):
        """Получить все привычки текущего пользователя с фильтрацией."""
        user_id = get_current_user_id()
        logger.info("[GET /habits] user=%s filters=%s", user_id, query_params)

        habits_query = Habit.query.filter_by(user_id=user_id)
        frequency = query_params.get("frequency")
        if frequency:
            logger.debug("Filtering by frequency=%s", frequency)
            habits_query = habits_query.filter_by(frequency=frequency)

        habits = habits_query.all()
        logger.info("[GET /habits] user=%s returned=%d habits", user_id, len(habits))
        return habits

    @habit_blp.arguments(HabitCreateSchema)
    @habit_blp.response(201, HabitSchema)
    @jwt_required()
    def post(self, new_data):
        """Создать новую привычку."""
        user_id = get_current_user_id()
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
        """Получить привычку по id."""
        user_id = get_current_user_id()
        logger.info("[GET /habits/%s] user=%s", habit_id, user_id)

        habit = get_user_habit_or_404(habit_id, user_id)
        logger.info("[GET /habits/%s] retrieved successfully", habit_id)
        return habit

    @habit_blp.arguments(HabitCreateSchema)
    @habit_blp.response(200, HabitSchema)
    @jwt_required()
    def patch(self, update_data, habit_id):
        """Обновить привычку по id."""
        user_id = get_current_user_id()
        logger.info(
            "[PATCH /habits/%s] user=%s update=%s", habit_id, user_id, update_data
        )

        habit = get_user_habit_or_404(habit_id, user_id)
        for key, value in update_data.items():
            logger.debug("Updating %s=%s", key, value)
            setattr(habit, key, value)

        db.session.commit()
        logger.info("[PATCH /habits/%s] updated successfully", habit_id)
        return habit

    @habit_blp.response(204)
    @jwt_required()
    def delete(self, habit_id):
        """Удалить привычку по id."""
        user_id = get_current_user_id()
        logger.warning("[DELETE /habits/%s] user=%s", habit_id, user_id)

        habit = get_user_habit_or_404(habit_id, user_id)
        db.session.delete(habit)
        db.session.commit()

        logger.info("[DELETE /habits/%s] deleted successfully", habit_id)
        return "", 204
