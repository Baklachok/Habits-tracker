from marshmallow import Schema, fields, validate


class HabitSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    description = fields.Str()
    frequency = fields.String(
        required=False, validate=lambda x: x in ("daily", "weekly")
    )
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class HabitCreateSchema(Schema):
    name = fields.Str(required=True)
    description = fields.Str()
    frequency = fields.String(
        required=False, validate=lambda x: x in ("daily", "weekly")
    )


class HabitQuerySchema(Schema):
    frequency = fields.String(
        required=False, validate=validate.OneOf(["daily", "weekly"])
    )
