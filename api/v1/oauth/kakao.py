import uuid

from fastapi import APIRouter, Request

from api.v1.Response import DefaultResponse
from api.v1.oauth.dto.token_response import TokenResponseData
from app.jwt.dto.token import UserLoginInfo
from app.jwt.service.oauth import KakaoAuthService
from fastapi.responses import JSONResponse
from app.jwt.decoder import AbstractJWTDecoder, JWTDecoder

from app.user.service.service import UserService

decoder: AbstractJWTDecoder = JWTDecoder()
kakao_router = APIRouter()
kakao_oauth_service = KakaoAuthService()
user_service = UserService()

@kakao_router.get("/login")
async def kakao_callback(request: Request):
    code: str = request.query_params.get("code")
    host: str = request.client.host
    user_info: UserLoginInfo = await kakao_oauth_service.do_login(host=host, code=code)

    payload = decoder.decode(token=user_info.access_token)
    user_id = uuid.UUID(payload.get("user_id"))

    is_user = user_service.find_user(user_id=user_id)
    if is_user is None:
        user_service.sign_up(user_id=user_id,
                             nickname=user_info.user_name)


    # response_data: TokenResponseData = TokenResponseData(
    #     access_token=user_info.access_token, user_name=user_info.user_name
    # )
    # response_body: DefaultResponse[TokenResponseData] = DefaultResponse.create_response(data=response_data, message="Login success")

    response_body = {
        "message" : "Login success",
        "data": {
            "access_token": user_info.access_token,
            "user_name": user_info.user_name
        }
    }
    response = JSONResponse(content=response_body, status_code=200)
    response.set_cookie(key="refresh_token", value=user_info.refresh_token, httponly=True, secure=True)
    return response

# @kakao_router.get("/logout")
# async def logout(request: Request):
#     await kakao_api.logout()
#     return RedirectResponse(url="/")
