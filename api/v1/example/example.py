from fastapi import APIRouter, Request, Depends

from core.fastapi.jwt_verifier import require_authorization, try_validate_token

example_router = APIRouter()

@example_router.get(path="")
async def hello_world(user_id: str = Depends(try_validate_token)):
    return "hello_world!"


@example_router.get(path="/protected")
async def hello_world(request: Request):
    return {"message":"protected hello_world!"}
