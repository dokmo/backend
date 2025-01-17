from fastapi import APIRouter

from api.v1.example.example import example_router
from api.v1.oauth.kakao import kakao_router
from api.v1.meet.meet_router import meet_router
from api.v1.user.user_router import user_router

api_router = APIRouter()
api_router.include_router(example_router, prefix="/example")
api_router.include_router(kakao_router, prefix="/kakao")
api_router.include_router(meet_router, prefix="/meet")
api_router.include_router(user_router, prefix="/user")