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
#FIXME(미들웨어의 토큰 검사에서 제외되어야해.)
@kakao_router.get("/callback")
async def kakao_callback(request: Request):
# async def kakao_callback(request: Request, code: str, error: str, error_description: str, state: str):
    code = request.query_params.get("code")
    token_info = await kakao_api.get_token(code)
    if "access_token" in token_info:
        user_info = await kakao_api.get_user_info(token_info.get("access_token"))
        users = {'userId':user_info.get('id')}
        # FIXME(userId가 존재할 경우 신규, 아닐경우 db에서 가져와야함.)
        # FIXME(userId가 db와 연결하여 데이터를 가져와야함. 그리고 토큰에 집어넣을거야. 우선 users를 일단 사용하자. 나중에 db에서 가져오는걸로 하고.)
        access_token = await jwt_service.create_access_token(data = users)
        refresh_token = await jwt_service.create_refresh_token(data = users)

        response = JSONResponse({"access_token": access_token})
        response.headers["Authorization"] = f"Bearer {access_token}"
        response.set_cookie(key="refresh_token", value=refresh_token, httponly=True, secure=True)

        # response = RedirectResponse(url="/", status_code=302)
        # FIXME(미들웨어에서 이 토큰을 사용할텐데 이 다음 과정을 어떻게 해야하지?)
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



#FIXME(TEST)
@kakao_router.get("/user_info")
async def get_user_info(request: Request):
    user_id = request.session.get("userId")
    return {user_id}


