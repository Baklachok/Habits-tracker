from app.models.user import User
from flask_jwt_extended import decode_token

from tests.factories import UserFactory
from tests.helpers import auth_headers


def test_register(client, db):
    """Регистрация нового пользователя"""
    payload = {"email": "test@example.com", "password": "password123"}

    resp = client.post("/auth/register", json=payload)
    data = resp.get_json()

    assert resp.status_code == 201
    assert data["email"] == payload["email"]

    # Проверяем, что пользователь реально добавлен в БД
    user = User.query.filter_by(email=payload["email"]).first()
    assert user is not None
    assert user.check_password("password123")


def test_register_existing_email(client, db):
    """Попытка зарегистрировать пользователя с существующим email"""
    UserFactory(email="test@example.com")
    db.session.commit()

    payload = {"email": "test@example.com", "password": "password123"}
    resp = client.post("/auth/register", json=payload)

    assert resp.status_code == 400


def test_login_success(client, db):
    """Успешный логин"""
    user = UserFactory()
    user.set_password("password123")
    db.session.commit()

    payload = {"email": user.email, "password": "password123"}
    resp = client.post("/auth/login", json=payload)
    data = resp.get_json()

    assert resp.status_code == 200
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["user"]["email"] == user.email

    # Проверяем, что токен валидный
    decoded = decode_token(data["access_token"])
    assert str(user.id) == decoded["sub"]


def test_login_wrong_password(client, db):
    """Логин с неверным паролем"""
    user = UserFactory()
    user.set_password("correct_password")
    db.session.commit()

    payload = {"email": user.email, "password": "wrong_password"}
    resp = client.post("/auth/login", json=payload)

    assert resp.status_code == 401


def test_me_endpoint(client, db):
    """Получение текущего пользователя через /me"""
    user = UserFactory()
    user.set_password("password123")
    db.session.commit()

    # Логинимся чтобы получить токен
    login_resp = client.post(
        "/auth/login", json={"email": user.email, "password": "password123"}
    )
    token = login_resp.get_json()["access_token"]

    resp = client.get(
        "/auth/me",
        headers=auth_headers(token),
    )
    data = resp.get_json()

    assert resp.status_code == 200
    assert data["email"] == user.email
