
from app.models.habit import Habit


def test_user_statistics_success(client, user, user_token, user_with_stats):
    """Корректная статистика при наличии привычек и логов."""
    resp = client.get(
        f"/api/statistics/user/{user.id}",
        headers={"Authorization": f"Bearer {user_token}"},
    )

    assert resp.status_code == 200
    data = resp.json

    # Базовые поля
    assert data["total_habits"] == 3
    assert "average_completion_rate" in data
    assert "top_habits" in data

    # Топ 3 привычек
    top = data["top_habits"]
    assert len(top) == 3

    # Сортировка по активности
    assert top[0]["completed_days"] >= top[1]["completed_days"]


def test_user_statistics_no_habits(client, user, user_token):
    """Если у пользователя нет ни одной привычки."""
    resp = client.get(
        f"/api/statistics/user/{user.id}",
        headers={"Authorization": f"Bearer {user_token}"},
    )

    assert resp.status_code == 200
    data = resp.json

    assert data["total_habits"] == 0
    assert data["average_completion_rate"] == 0
    assert data["top_habits"] == []


def test_user_statistics_no_logs(client, user, user_token, db):
    """Если есть привычки, но нет логов."""
    habits = [
        Habit(name="H1", user_id=user.id),
        Habit(name="H2", user_id=user.id),
    ]
    db.session.add_all(habits)
    db.session.commit()

    resp = client.get(
        f"/api/statistics/user/{user.id}",
        headers={"Authorization": f"Bearer {user_token}"},
    )

    assert resp.status_code == 200
    data = resp.json

    assert data["total_habits"] == 2
    assert data["average_completion_rate"] == 0
    assert data["top_habits"] == []


def test_user_statistics_unauthorized(client, user):
    """Без токена должен возвращаться 401."""
    resp = client.get(f"/api/statistics/user/{user.id}")
    assert resp.status_code == 401
