from typing import Type

from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

db: SQLAlchemy = SQLAlchemy()
BaseModel: Type = db.Model
jwt = JWTManager()
