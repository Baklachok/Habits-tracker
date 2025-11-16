from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity

from app import db
from app.models.habit import Habit
from app.models.habit_log import HabitLog
from app.schemas.habit import HabitSchema, HabitCreateSchema, HabitQuerySchema
from app.schemas.habit_stats import HabitStatsSchema

habit_blp = Blueprint("habits", __name__, description="CRUD operations for habits")


@habit_blp.route("/")
class HabitListResource(MethodView):
    @habit_blp.arguments(HabitQuerySchema, location="query")
    @habit_blp.response(200, HabitSchema(many=True))
    @jwt_required()
    def get(self, query_params):
        """Get all habits for current user"""
        user_id = int(get_jwt_identity())
        frequency = query_params.get("frequency")
        habits = Habit.query.filter_by(user_id=user_id)
        if frequency:
            habits = habits.filter_by(frequency=frequency)
        return habits.all()

    @habit_blp.arguments(HabitCreateSchema)
    @habit_blp.response(201, HabitSchema)
    @jwt_required()
    def post(self, new_data):
        """Create a new habit"""
        user_id = int(get_jwt_identity())
        habit = Habit(user_id=user_id, **new_data)
        db.session.add(habit)
        db.session.commit()
        return habit


@habit_blp.route("/<int:habit_id>")
class HabitResource(MethodView):
    @habit_blp.response(200, HabitSchema)
    @jwt_required()
    def get(self, habit_id):
        """Get habit by id"""
        user_id = int(get_jwt_identity())
        habit = Habit.query.filter_by(id=habit_id, user_id=user_id).first_or_404()
        return habit

    @habit_blp.arguments(HabitCreateSchema)
    @habit_blp.response(200, HabitSchema)
    @jwt_required()
    def patch(self, update_data, habit_id):
        """Update habit by id"""
        user_id = int(get_jwt_identity())
        habit = Habit.query.filter_by(id=habit_id, user_id=user_id).first_or_404()
        habit.name = update_data.get("name", habit.name)
        habit.description = update_data.get("description", habit.description)
        db.session.commit()
        return habit

    @habit_blp.response(204)
    @jwt_required()
    def delete(self, habit_id):
        """Delete habit by id"""
        user_id = int(get_jwt_identity())
        habit = Habit.query.filter_by(id=habit_id, user_id=user_id).first_or_404()
        db.session.delete(habit)
        db.session.commit()
        return "", 204


@habit_blp.route("/<int:habit_id>/stats")
class HabitStatsResource(MethodView):
    @habit_blp.response(200, HabitStatsSchema)
    @jwt_required()
    def get(self, habit_id):
        """Return progress statistics for a habit"""
        user_id = int(get_jwt_identity())

        habit = Habit.query.filter_by(id=habit_id, user_id=user_id).first_or_404()

        logs = (
            HabitLog.query.filter_by(habit_id=habit.id, user_id=user_id)
            .order_by(HabitLog.date.asc())
            .all()
        )

        from app.services.habit_stats import (
            calculate_streak,
            calculate_completion_rate,
        )

        return {
            "habit_id": habit.id,
            "streak": calculate_streak(logs),
            "completion_rate": calculate_completion_rate(logs),
        }
