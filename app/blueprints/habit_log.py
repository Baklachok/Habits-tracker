import logging
from flask_smorest import Blueprint
from flask.views import MethodView
from flask_jwt_extended import jwt_required

from app import db
from app.models.habit_log import HabitLog
from app.schemas.habit_log import HabitLogSchema
from app.utils.mixins import HabitLogMixin

logger = logging.getLogger(__name__)

habit_log_blp = Blueprint(
    "HabitLogs",
    "habit_logs",
    url_prefix="/habit_logs",
    description="CRUD for habit logs",
)


@habit_log_blp.route("/")
class HabitLogListResource(MethodView, HabitLogMixin):
    @habit_log_blp.response(200, HabitLogSchema(many=True))
    @jwt_required()
    def get(self):
        user_id = self._get_user_id()
        logger.info("Fetching all habit logs for user_id=%s", user_id)

        logs = HabitLog.query.filter_by(user_id=user_id).all()
        logger.debug("Found %s logs for user_id=%s", len(logs), user_id)
        return logs

    @habit_log_blp.arguments(HabitLogSchema)
    @habit_log_blp.response(201, HabitLogSchema)
    @jwt_required()
    def post(self, new_data):
        user_id = self._get_user_id()
        logger.info("Creating new habit log for user_id=%s", user_id)
        logger.debug("Payload: %s", new_data)

        log = HabitLog(user_id=user_id, **new_data)
        db.session.add(log)
        db.session.commit()

        logger.info("Habit log created: log_id=%s, user_id=%s", log.id, user_id)
        return log


@habit_log_blp.route("/<int:log_id>")
class HabitLogResource(MethodView, HabitLogMixin):
    @habit_log_blp.response(200, HabitLogSchema)
    @jwt_required()
    def get(self, log_id):
        user_id = self._get_user_id()
        logger.info("Fetching habit log: log_id=%s, user_id=%s", log_id, user_id)

        log = self._get_log_or_404(log_id, user_id)
        logger.debug("Habit log found: %s", log)
        return log

    @habit_log_blp.arguments(HabitLogSchema(partial=True))
    @habit_log_blp.response(200, HabitLogSchema)
    @jwt_required()
    def patch(self, updated_data, log_id):
        user_id = self._get_user_id()
        logger.info("Updating habit log: log_id=%s, user_id=%s", log_id, user_id)
        logger.debug("Update payload: %s", updated_data)

        log = self._get_log_or_404(log_id, user_id)
        for key, value in updated_data.items():
            setattr(log, key, value)
        db.session.commit()

        logger.info("Habit log updated: log_id=%s, user_id=%s", log_id, user_id)
        return log

    @habit_log_blp.response(204)
    @jwt_required()
    def delete(self, log_id):
        user_id = self._get_user_id()
        logger.warning("Deleting habit log: log_id=%s, user_id=%s", log_id, user_id)

        log = self._get_log_or_404(log_id, user_id)
        db.session.delete(log)
        db.session.commit()

        logger.info("Habit log deleted: log_id=%s, user_id=%s", log_id, user_id)
        return "", 204
