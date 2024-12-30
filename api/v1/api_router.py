from fastapi import APIRouter
from api.v1.example.example import example_router

api_router = APIRouter()
api_router.include_router(example_router, prefix="/example")