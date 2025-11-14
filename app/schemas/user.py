from marshmallow import Schema, fields


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    email = fields.Email(required=True)


class RegisterSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)


class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)


class CreateUserSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)
