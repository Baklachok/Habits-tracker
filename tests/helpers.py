import datetime

from app.models.habit_log import HabitLog


def auth_headers(token: str) -> dict:
    """Возвращает словарь headers с Bearer-токеном"""
    return {"Authorization": f"Bearer {token}"}


def create_log(db, habit, completed=False, date=None):
    """Хелпер для создания HabitLog в БД"""
    if date is None:
        date = datetime.date.today()
    log = HabitLog(
        habit_id=habit.id, user_id=habit.user_id, date=date, completed=completed
    )
    db.session.add(log)
    db.session.commit()
    return log
