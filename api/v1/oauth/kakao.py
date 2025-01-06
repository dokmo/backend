from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from app.jwt.service.service import JWTService
from core.utils.kakao_manager import KakaoAPI


kakao_router = APIRouter()
kakao_api = KakaoAPI()
jwt_service = JWTService()

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
        user_info = await kakao_api.get_user_info(token_info.get("access_token"))
        # 토큰 발급
        users = {'userId':user_info.get('id')}
        # token = await jwt_service.create_access_token(data = users)
        # print(token)
        # decoded_token = await jwt_service.check_token_expired(token)
        # print(decoded_token)
        # FIXME("에러 발생에 따른 방법은?")
        return RedirectResponse(url="/user_info", status_code=302)
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


