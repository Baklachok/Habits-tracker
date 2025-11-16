import pytest
from app import create_app, db as _db
from flask_jwt_extended import create_access_token


@pytest.fixture(scope="session")
def app():
    app = create_app(testing=True)

    # Подменяем БД на SQLite in-memory
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["TESTING"] = True

    with app.app_context():
        _db.create_all()

    yield app

    # teardown (session)
    with app.app_context():
        _db.drop_all()


@pytest.fixture(autouse=True)
def clean_db(db):
    """Очистка всех таблиц перед каждым тестом"""
    db.session.remove()
    for table in reversed(db.metadata.sorted_tables):
        db.session.execute(table.delete())
    db.session.commit()


@pytest.fixture()
def db(app):
    """Provide a clean database for each test."""
    with app.app_context():
        _db.session.begin_nested()
        yield _db
        _db.session.rollback()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def user_token(app, db):
    """Create a user and return JWT token."""
    from app.models.user import User

    user = User(email="test@example.com")
    user.set_password("password123")
    db.session.add(user)
    db.session.commit()

    token = create_access_token(identity=str(user.id))

    return token
