from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from app.jwt.service.service import JWTService
from app.jwt.schemas.decoder import JWTDecoder
from app.jwt.schemas.encoder import JWTEncoder
from core.utils.kakao_manager import KakaoAPI


kakao_router = APIRouter()
kakao_api = KakaoAPI()
jwt_service = JWTService(JWTEncoder, JWTDecoder)

@kakao_router.get("/login")
def get_kakao_code(request: Request):
    scope = 'profile_nickname, profile_image'           # 요청할 권한 범위
    kakao_auth_url = kakao_api.getcode_auth_url(scope)
    return RedirectResponse(kakao_auth_url)


# 카카오 로그인 후 카카오에서 리디렉션될 엔드포인트
# 카카오에서 제공한 인증 코드를 사용하여 액세스 토큰을 요청
@kakao_router.get("/callback")
async def kakao_callback(request: Request, code: str):
    token_info = await kakao_api.get_token(code)

    # FIXME("받은 정보로 해야할 일이 무엇이 있는지?")


    if "access_token" in token_info:
        request.session['access_token'] = token_info['access_token']
        return RedirectResponse(url="/user_info", status_code=302)
    else:
        return RedirectResponse(url="/?error=Failed to authenticate", status_code=302)



@kakao_router.get("/logout")
async def logout(request: Request):
    client_id = kakao_api.client_id
    logout_redirect_uri = kakao_api.logout_redirect_uri
    await kakao_api.logout(client_id, logout_redirect_uri)
    # FIXME("로그아웃때 jwt는 무엇을 해야하는지?.")
    return RedirectResponse(url="/")


