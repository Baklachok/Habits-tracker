import factory
from datetime import date
from app import db
from app.models.habit import Habit
from app.models.habit_log import HabitLog
from app.models.user import User


class HabitFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Habit
        sqlalchemy_session = db.session

    id = factory.Sequence(lambda n: n + 1)
    user_id = 1
    name = "Drink water"
    description = "Drink 2 liters daily"
    frequency = "daily"


class HabitLogFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = HabitLog
        sqlalchemy_session = db.session

    id = factory.Sequence(lambda n: n + 1)
    habit_id = 1
    user_id = 1
    date = factory.LazyFunction(lambda: date.today())
    completed = True


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "flush"

    id = factory.Sequence(lambda n: n + 1)
    email = factory.Sequence(lambda n: f"user{n}@example.com")
    password_hash = factory.LazyFunction(
        lambda: User.set_password_static("password123")
    )
