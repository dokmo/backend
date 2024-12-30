from uuid import uuid4
from fastapi import Request, Form, HTTPException, APIRouter
from starlette.middleware.sessions import SessionMiddleware
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from kakao_manager import KakaoAPI  # KakaoAPI 클래스를 다른 파일에서 임포트

kakao_router = APIRouter()

# # 1. 세션 미들웨어를 앱에 추가, 'your-secret-key'는 실제 프로덕션에서는 안전한 값으로 변경해야함.
# kakao_router.add_middleware(SessionMiddleware, secret_key=str(uuid4()))
"""
어떤 역할을 하지?
어떻게 리팩토링 해서 집어넣어야 하지?

secret_key가 뭐길래?
-> 세션 암호화를 위한 비밀 키.

DELETEME
"""


# 2. Jinja2 템플릿 엔진을 설정 (for test)
templates = Jinja2Templates(directory="templates")

# KakaoAPI 인스턴스를 생성
kakao_api = KakaoAPI()

# 카카오 로그인을 시작하기 위한 엔드포인트
# 사용자를 카카오 인증 URL로 리다이렉트
@kakao_router.get("/getcode")
def get_kakao_code(request: Request):
    scope = 'profile_nickname, profile_image'  # 요청할 권한 범위
    kakao_auth_url = kakao_api.getcode_auth_url(scope)
    return RedirectResponse(kakao_auth_url)

# 카카오 로그인 후 카카오에서 리디렉션될 엔드포인트
# 카카오에서 제공한 인증 코드를 사용하여 액세스 토큰을 요청
@kakao_router.get("/callback")
async def kakao_callback(request: Request, code: str):
    token_info = await kakao_api.get_token(code)
    if "access_token" in token_info:
        request.session['access_token'] = token_info['access_token']
        return RedirectResponse(url="/user_info", status_code=302)
    else:
        return RedirectResponse(url="/?error=Failed to authenticate", status_code=302)

# 홈페이지 및 로그인/로그아웃 버튼을 표시
@kakao_router.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    logged_in = 'access_token' in request.session
    return templates.TemplateResponse("index.html", {"request": request, "client_id": kakao_api.client_id, "redirect_uri": kakao_api.redirect_uri, "logged_in": logged_in})


# 로그인 처리를 위한 엔드포인트
# 이 예제에서는 사용되지 않으며, `/callback` 엔드포인트가 이 역할을 대신
@kakao_router.post("/login")
async def login(request: Request, code: str = Form(...)):
    raise HTTPException(status_code=400, detail="Kakao login failed")
"""
이건 무슨말이지?
/login으로 하면 오류를 일부러 내는거라고?
DELETEME
"""


# 로그아웃 처리를 위한 엔드포인트
# 세션에서 액세스 토큰을 제거하고 홈페이지로 리다이렉트
@kakao_router.get("/logout")
async def logout(request: Request):
    client_id = kakao_api.client_id
    logout_redirect_uri = kakao_api.logout_redirect_uri
    await kakao_api.logout(client_id, logout_redirect_uri)
    request.session.pop('access_token', None)
    return RedirectResponse(url="/")

# 사용자 정보를 표시하기 위한 엔드포인트
# 세션에 저장된 액세스 토큰을 사용하여 카카오 API에서 사용자 정보를 가져옴
@kakao_router.get("/user_info", response_class=HTMLResponse)
async def user_info(request: Request):
    access_token = request.session.get('access_token')
    if access_token:
        user_info = await kakao_api.get_user_info(access_token)
        return templates.TemplateResponse("user_info.html", {"request": request, "user_info": user_info})
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")

# 액세스 토큰을 새로고침하기 위한 엔드포인트
@kakao_router.post("/refresh_token")
async def refresh_token(refresh_token: str = Form(...)):
    client_id = kakao_api.client_id
    new_token_info = await kakao_api.refreshAccessToken(client_id, refresh_token)
    return new_token_info