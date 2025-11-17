from flask_jwt_extended import get_jwt_identity

from app.models.habit_log import HabitLog


class HabitLogMixin:
    """Вспомогательные методы для HabitLogResource"""

    @staticmethod
    def _get_user_id() -> int:
        return get_jwt_identity()

    @staticmethod
    def _get_log_or_404(log_id: int, user_id: int) -> HabitLog:
        return HabitLog.query.filter_by(id=log_id, user_id=user_id).first_or_404()
