from fastapi import APIRouter
from api.v1.example.example import example_router
from api.v1.oauth.kakao import kakao_router

api_router = APIRouter()
api_router.include_router(example_router, prefix="/example")
api_router.include_router(kakao_router, prefix="/kakao")