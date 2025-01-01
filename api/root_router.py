from fastapi import APIRouter
from api.v1.api_router import api_router

root_router = APIRouter()
root_router.include_router(api_router, prefix="/api")