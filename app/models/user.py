from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from werkzeug.security import generate_password_hash, check_password_hash

from app.extentions import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    def __repr__(self):
        return f"<User {self.email}>"

    # Методы для безопасного хранения пароля
    def set_password(self, password: str):
        """Хэширует и сохраняет пароль."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Проверяет пароль пользователя."""
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {"id": self.id, "email": self.email}

    @staticmethod
    def set_password_static(password):
        u = User()
        u.set_password(password)
        return u.password_hash
