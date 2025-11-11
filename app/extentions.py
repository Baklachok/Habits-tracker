from typing import Type

from flask_sqlalchemy import SQLAlchemy

db: SQLAlchemy = SQLAlchemy()
BaseModel: Type = db.Model
