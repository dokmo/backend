from fastapi import APIRouter

user_router = APIRouter()

@user_router.post(path="/register")
async def sign_up():
    ...