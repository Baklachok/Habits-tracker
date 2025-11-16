from tests.factories import HabitFactory
from tests.helpers import auth_headers


def test_create_habit(client, db, user_token):
    response = client.post(
        "/habits/",
        json={"name": "Run", "description": "Run 3km", "frequency": "daily"},
        headers=auth_headers(user_token),
    )

    assert response.status_code == 201
    data = response.get_json()
    assert data["name"] == "Run"


def test_get_habits(client, db, user_token):
    HabitFactory.create_batch(3)
    db.session.commit()

    response = client.get("/habits/", headers=auth_headers(user_token))

    assert response.status_code == 200
    assert len(response.get_json()) == 3


def test_filter_habits_by_frequency(client, db, user_token):
    HabitFactory(frequency="daily")
    HabitFactory(frequency="weekly")
    db.session.commit()

    response = client.get("/habits/?frequency=daily", headers=auth_headers(user_token))
    data = response.get_json()

    assert response.status_code == 200
    assert len(data) == 1
    assert data[0]["frequency"] == "daily"


def test_get_single_habit(client, db, user_token):
    habit = HabitFactory()
    db.session.commit()

    response = client.get(f"/habits/{habit.id}", headers=auth_headers(user_token))
    data = response.get_json()

    assert response.status_code == 200
    assert data["id"] == habit.id
    assert data["name"] == habit.name


def test_get_habit_404_not_owner(client, db, user_token):
    habit = HabitFactory(user_id=999)
    db.session.commit()

    response = client.get(f"/habits/{habit.id}", headers=auth_headers(user_token))
    assert response.status_code == 404


def test_update_habit(client, db, user_token):
    habit = HabitFactory(name="Old", description="Old desc")
    db.session.commit()

    response = client.patch(
        f"/habits/{habit.id}",
        json={"name": "New", "description": "New desc", "frequency": "daily"},
        headers=auth_headers(user_token),
    )
    data = response.get_json()

    assert response.status_code == 200
    assert data["name"] == "New"
    assert data["description"] == "New desc"


def test_update_habit_not_owner(client, db, user_token):
    habit = HabitFactory(user_id=999)
    db.session.commit()

    response = client.patch(
        f"/habits/{habit.id}",
        json={"name": "Changed"},
        headers=auth_headers(user_token),
    )
    assert response.status_code == 404


def test_delete_habit(client, db, user_token):
    habit = HabitFactory()
    db.session.commit()

    response = client.delete(f"/habits/{habit.id}", headers=auth_headers(user_token))
    assert response.status_code == 204
    assert db.session.get(type(habit), habit.id) is None


def test_delete_habit_not_owner(client, db, user_token):
    habit = HabitFactory(user_id=999)
    db.session.commit()

    response = client.delete(f"/habits/{habit.id}", headers=auth_headers(user_token))
    assert response.status_code == 404


def test_create_habit_invalid(client, db, user_token):
    """Validation error: missing name"""
    response = client.post(
        "/habits/",
        json={"description": "Missing name"},
        headers=auth_headers(user_token),
    )
    assert response.status_code == 422
