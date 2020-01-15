from jetkit.api.auth import blp, use_core_auth_api  # noqa: F401
from TEMPLATE.model.user import User
from .schema import UserSchema

use_core_auth_api(auth_model=User, user_schema=UserSchema)
