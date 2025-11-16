from flask_smorest import Blueprint
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity

from app import db
from app.models.habit_log import HabitLog
from app.schemas.habit_log import HabitLogSchema

habit_log_blp = Blueprint(
    "HabitLogs",
    "habit_logs",
    url_prefix="/habit_logs",
    description="CRUD for habit logs",
)


@habit_log_blp.route("/")
class HabitLogListResource(MethodView):
    @habit_log_blp.response(200, HabitLogSchema(many=True))
    @jwt_required()
    def get(self):
        """Получить все логи текущего пользователя"""
        user_id = get_jwt_identity()
        return HabitLog.query.filter_by(user_id=user_id).all()

    @habit_log_blp.arguments(HabitLogSchema)
    @habit_log_blp.response(201, HabitLogSchema)
    @jwt_required()
    def post(self, new_data):
        """Создать новый лог"""
        user_id = get_jwt_identity()
        log = HabitLog(user_id=user_id, **new_data)
        db.session.add(log)
        db.session.commit()
        return log


@habit_log_blp.route("/<int:log_id>")
class HabitLogResource(MethodView):
    @habit_log_blp.response(200, HabitLogSchema)
    @jwt_required()
    def get(self, log_id):
        """Получить конкретный лог"""
        user_id = get_jwt_identity()
        log = HabitLog.query.filter_by(id=log_id, user_id=user_id).first_or_404()
        return log

    @habit_log_blp.arguments(HabitLogSchema(partial=True))
    @habit_log_blp.response(200, HabitLogSchema)
    @jwt_required()
    def patch(self, updated_data, log_id):
        """Обновить лог"""
        user_id = get_jwt_identity()
        log = HabitLog.query.filter_by(id=log_id, user_id=user_id).first_or_404()
        for key, value in updated_data.items():
            setattr(log, key, value)
        db.session.commit()
        return log

    @habit_log_blp.response(204)
    @jwt_required()
    def delete(self, log_id):
        """Удалить лог"""
        user_id = get_jwt_identity()
        log = HabitLog.query.filter_by(id=log_id, user_id=user_id).first_or_404()
        db.session.delete(log)
        db.session.commit()
        return "", 204
