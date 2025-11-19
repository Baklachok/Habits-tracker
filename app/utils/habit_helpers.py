from flask_jwt_extended import get_jwt_identity
from app.models.habit import Habit


def get_current_user_id() -> int:
    """Возвращает id текущего пользователя из JWT."""
    return int(get_jwt_identity())


def get_user_habit_or_404(habit_id: int, user_id: int) -> Habit:
    """Возвращает привычку пользователя или вызывает 404."""
    return Habit.query.filter_by(id=habit_id, user_id=user_id).first_or_404()
