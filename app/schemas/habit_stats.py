from marshmallow import Schema, fields


class HabitStatsSchema(Schema):
    habit_id = fields.Int()
    streak = fields.Int()
    completion_rate = fields.Float()
