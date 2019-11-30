from jetkit.api.auth import CoreAuthAPI, blp  # noqa: F401
from TEMPLATE.model.user import User
from .schema import UserSchema

CoreAuthAPI(auth_model=User, user_schema=UserSchema)
