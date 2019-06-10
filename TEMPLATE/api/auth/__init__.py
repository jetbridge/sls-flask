from flask_rest_api import Blueprint, abort
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required,
    jwt_required,
    get_current_user,
)
from TEMPLATE.model.user import User
from .schema import LoginRequest, AuthResponse, TokenRefreshResponseSchema

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


@blp.route("refresh", methods=["POST"])
@jwt_refresh_token_required
@blp.response(TokenRefreshResponseSchema)
def refresh_token():
    current_user = get_current_user()
    return {"access_token": create_access_token(identity=current_user)}


@blp.route("check")
@jwt_required
def check_auth():
    return "ok"
