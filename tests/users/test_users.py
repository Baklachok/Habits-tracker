from tests.factories import UserFactory


def test_get_users_empty(client, db):
    """Если пользователей нет, возвращается пустой список"""
    response = client.get("/api/users")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 0


def test_get_users_with_data(client, db):
    """Проверка, что эндпоинт возвращает существующих пользователей"""
    # создаем 3 пользователя через фабрику
    UserFactory.create_batch(3)
    db.session.commit()

    response = client.get("/api/users")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 3

    # проверяем структуру первого пользователя
    user_data = data[0]
    assert "id" in user_data
    assert "email" in user_data


def test_get_users_data_matches_db(client, db):
    """Проверяем, что данные в ответе совпадают с базой"""
    UserFactory(email="test@example.com")
    db.session.commit()

    response = client.get("/api/users")
    data = response.get_json()
    assert len(data) == 1
    assert data[0]["email"] == "test@example.com"
