import datetime
from app.models.habit_log import HabitLog
from tests.factories import HabitFactory
from tests.helpers import auth_headers, create_log


def test_get_empty_logs(client, db, user_token):
    """GET /habit_logs когда логов нет"""
    resp = client.get("/habit_logs/", headers=auth_headers(user_token))
    assert resp.status_code == 200
    assert resp.get_json() == []


def test_create_habit_log(client, db, user_token):
    """POST /habit_logs"""
    habit = HabitFactory(user_id=1)
    db.session.commit()

    payload = {
        "habit_id": habit.id,
        "date": str(datetime.date.today()),
        "completed": True,
    }
    resp = client.post("/habit_logs/", json=payload, headers=auth_headers(user_token))
    data = resp.get_json()

    assert resp.status_code == 201
    assert data["habit_id"] == habit.id
    assert data["completed"] is True

    # Проверка в БД
    log = HabitLog.query.get(data["id"])
    assert log is not None


def test_get_specific_log(client, db, user_token):
    """GET /habit_logs/<log_id>"""
    habit = HabitFactory()
    db.session.commit()
    log = create_log(db, habit, completed=True)

    resp = client.get(f"/habit_logs/{log.id}", headers=auth_headers(user_token))
    data = resp.get_json()

    assert resp.status_code == 200
    assert data["id"] == log.id
    assert data["completed"] is True


def test_update_habit_log(client, db, user_token):
    """PATCH /habit_logs/<log_id>"""
    habit = HabitFactory()
    db.session.commit()
    log = create_log(db, habit, completed=False)

    resp = client.patch(
        f"/habit_logs/{log.id}",
        json={"completed": True},
        headers=auth_headers(user_token),
    )
    data = resp.get_json()

    assert resp.status_code == 200
    assert data["completed"] is True

    log_db = HabitLog.query.get(log.id)
    assert log_db.completed is True


def test_delete_habit_log(client, db, user_token):
    """DELETE /habit_logs/<log_id>"""
    habit = HabitFactory()
    db.session.commit()
    log = create_log(db, habit, completed=True)

    resp = client.delete(f"/habit_logs/{log.id}", headers=auth_headers(user_token))
    assert resp.status_code == 204

    assert HabitLog.query.get(log.id) is None
