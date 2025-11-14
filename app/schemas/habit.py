from marshmallow import Schema, fields


class HabitSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    description = fields.Str()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class HabitCreateSchema(Schema):
    name = fields.Str(required=True)
    description = fields.Str()
