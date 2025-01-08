import uuid

from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from app.jwt.service.service import JWTService
from core.utils.kakao_manager import KakaoAPI
from fastapi.responses import JSONResponse

kakao_router = APIRouter()
kakao_api = KakaoAPI()
jwt_service = JWTService()

#FIXME(미들웨어의 토큰 검사에서 제외되어야해.)
@kakao_router.get("/login")
async def get_kakao_code(request: Request):
    scope = 'profile_nickname, profile_image'           # 요청할 권한 범위 https://developers.kakao.com/console/app/1182284/product/login/scope
    kakao_auth_url = kakao_api.getcode_auth_url(scope)
    return RedirectResponse(kakao_auth_url)


# 카카오 로그인 후 카카오에서 리디렉션될 엔드포인트
# 카카오에서 제공한 인증 코드를 사용하여 액세스 토큰을 요청
@kakao_router.get("/callback")
async def kakao_callback(request: Request):
# async def kakao_callback(request: Request, code: str, error: str, error_description: str, state: str):
    code = request.query_params.get("code")
    token_info = await kakao_api.get_token(code)
    if "access_token" in token_info:
        # kakao 고유 유저 id 획득
        user_info = await kakao_api.get_user_info(token_info.get("access_token"))

        # # FIXME(userId가 존재할 경우 신규, 아닐경우 db에서 가져와야함.)
        # kakao_user_id = user_info.get('id')
        # # db로 부터 유저 확인. kakaoid가 없으면 해당 유저를 추가시키고, 있으면 해당 user_id를 가져옴.
        # user = await user_service.(kakao_user_id=kakao_user_id)
        # if not user:
        #     #유저 추가
        # user_id = user.user_id
        # users = {'user_id':user_id}

        user_id = str(uuid.uuid4())
        kakao_user_nickname = user_info.get('properties').get('nickname')

        user = {'user_id':user_id} #FIXME(uuid구현 전까지 일단 kakao_user_id 사용.)

        access_token = await jwt_service.create_access_token(data = user)
        refresh_token = await jwt_service.create_refresh_token(data = user)

        # 응답에 토큰과 사용자 ID 설정 FIXME(임시 테스트용 코드. userId를 kakao id 가 아닌 userid(UUID)로 바꾸어야함.)
        response_data = {
            'message': 'Success',
            'data': {
                'access_token': access_token,
                'user_nickname': kakao_user_nickname
            }
        }
        # response = RedirectResponse(url="/", status_code=200)
        response = JSONResponse(content=response_data, status_code=200)
        response.set_cookie(key="refresh_token", value=refresh_token, httponly=True, secure=True)

        return response
    else:
        return RedirectResponse(url="/?error=Failed to authenticate", status_code=302)


@kakao_router.get("/logout")
async def logout(request: Request):
    client_id = kakao_api.client_id
    logout_redirect_uri = kakao_api.logout_redirect_uri
    await kakao_api.logout(client_id, logout_redirect_uri)
    # FIXME("로그아웃때 jwt는 무엇을 해야하는지?")
    # FIXME("same site option?? None이 아니라 다른걸로 바뀜.")
    return RedirectResponse(url="/")


@kakao_router.get("/user_info")
async def user_info(request: Request):
    user_id = request.scope.get("user_id")
    refresh_token = request.cookies.get("refresh_token")
    messages = {
        "user_id": user_id,
        "refresh_token": refresh_token,
    }

    return messages

