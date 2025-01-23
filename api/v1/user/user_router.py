from fastapi import APIRouter, Depends
from app.user.service.service import UserService
from core.fastapi.jwt_verifier import try_validate_token, require_authorization
import uuid
user_router = APIRouter()
user_service = UserService()

@user_router.get(path="")
async def get_user(
        user_id: uuid.UUID = Depends(require_authorization)
):
    from app.user.domain.user import User
    user: User = await user_service.find_user(user_id=user_id)