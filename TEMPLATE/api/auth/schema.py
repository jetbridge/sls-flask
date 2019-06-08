from marshmallow import fields as f, Schema


class LoginRequest(Schema):
    email = f.String(required=True, allow_none=False)
    password = f.String(required=True, allow_none=False)


class AuthResponse(Schema):
    access_token = f.String()
    refresh_token = f.String()


class TokenRefreshRequestSchema(Schema):
    token = f.String(required=True, allow_none=False)
