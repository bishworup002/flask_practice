from marshmallow import Schema, fields, validate

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True, validate=validate.Length(min=3, max=64))
    first_name = fields.Str(required=True, validate=validate.Length(min=1, max=64))
    last_name = fields.Str(required=True, validate=validate.Length(min=1, max=64))
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True, validate=validate.Length(min=6))
    role = fields.Str(validate=validate.OneOf(['admin', 'user']))
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    is_active = fields.Boolean()

class UserUpdateSchema(Schema):
    first_name = fields.Str(validate=validate.Length(min=1, max=64))
    last_name = fields.Str(validate=validate.Length(min=1, max=64))
    email = fields.Email()
    password = fields.Str(load_only=True, validate=validate.Length(min=6))
    is_active = fields.Boolean()

class AuthSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)

class PasswordResetRequestSchema(Schema):
    email = fields.Email(required=True)

class PasswordResetSchema(Schema):
    token = fields.Str(required=True)
    new_password = fields.Str(required=True, validate=validate.Length(min=6))