from datetime import datetime

from app import db
from app.extentions import BaseModel


class HabitLog(BaseModel):
    __tablename__ = "habit_logs"

    id = db.Column(db.Integer, primary_key=True)
    habit_id = db.Column(db.Integer, db.ForeignKey("habits.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    date = db.Column(db.Date, default=datetime.utcnow, nullable=False)
    completed = db.Column(db.Boolean, default=False)

    habit = db.relationship("Habit", backref="logs")
    user = db.relationship("User", backref="habit_logs")
