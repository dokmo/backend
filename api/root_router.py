from fastapi import APIRouter
from api.v1.api_router import api_router
from api.v1.oauth.login import kakao_router

root_router = APIRouter()
root_router.include_router(api_router, prefix="/api")
root_router.include_router(kakao_router, prefix="/login")