from marshmallow import Schema, fields


class HabitLogSchema(Schema):
    id = fields.Int(dump_only=True)
    habit_id = fields.Int(required=True)
    user_id = fields.Int(dump_only=True)
    date = fields.Date()
    completed = fields.Bool()
