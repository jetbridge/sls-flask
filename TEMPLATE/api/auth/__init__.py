from flask_rest_api import Blueprint, abort
from flask_jwt_extended import create_access_token, create_refresh_token
from TEMPLATE.model.user import User
from .schema import LoginRequest, AuthResponse, TokenRefreshRequestSchema
from flask import current_app

blp = Blueprint("Authentication", __name__, url_prefix="/api/auth")


def auth_response_for_user(user):
    access_token = create_access_token(identity=user)
    refresh_token = create_refresh_token(identity=user)
    return {"access_token": access_token, "refresh_token": refresh_token}


@blp.route("login", methods=["POST"])
@blp.arguments(LoginRequest, as_kwargs=True)
@blp.response(AuthResponse)
def login(email: str, password: str):
    """Login with username + password."""
    user = User.query.filter_by(email=email).one_or_none()
    if not user or not user.is_correct_password(password):
        abort(401, message="Wrong user name or password")
    return auth_response_for_user(user)


@blp.route("refresh_token", methods=["POST"])
@blp.arguments(TokenRefreshRequestSchema(), as_kwargs=True)
@blp.response(AuthResponse)
def refresh_token(token: str):
    secret = current_app.config.get("JWT_SECRET_KEY")
    try:
        decoded_token = jwt.decode(token, secret, algorithms=["HS256"])
        user_id = decoded_token.get("identity")
        if decoded_token.get("type") != "refresh":
            abort(401, message="Wrong token type")
        user = User.query.get_or_404(user_id)
        return auth_response_for_user(user)
    except jwt.ExpiredSignature:
        abort(401, message="Signature Expired")
