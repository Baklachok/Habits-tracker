import pytest

from app import create_app, db as _db


pytest_plugins = [
    "tests.fixtures.users",
    "tests.fixtures.habits",
    "tests.fixtures.logs",
    "tests.fixtures.statistics",
]


# ===============================
# Application fixture
# ===============================
@pytest.fixture(scope="session")
def app():
    """Create and configure a Flask app instance for testing."""
    app = create_app(testing=True)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["TESTING"] = True

    with app.app_context():
        _db.create_all()

    yield app

    with app.app_context():
        _db.drop_all()


# ===============================
# Database fixtures
# ===============================
@pytest.fixture(autouse=True)
def clean_db(db):
    """Clean all tables before each test."""
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


# ===============================
# Test client fixture
# ===============================
@pytest.fixture()
def client(app):
    """Flask test client."""
    return app.test_client()
