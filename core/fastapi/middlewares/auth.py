from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from starlette.datastructures import Headers
from starlette.types import ASGIApp, Receive, Scope, Send
from jose import jwt, JWTError
from core.config.config import loader

class VerifyTokenMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp) -> None:
        super().__init__(app)
        self.secret_key = loader.config.SECRET_KEY
        self.algorithm = loader.config.ALGORITHM

    def extract_token(self, headers: Headers) -> str:
        auth_header = headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise JWTError("Authorization header missing or invalid")
        return auth_header[len("Bearer "):]

    def verify_token(self, token: str) -> dict:
        return jwt.decode(token, self.secret_key, algorithms=[self.algorithm], options={"verify_exp": True})

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        # 요청된 엔드포인트 확인
        route = scope.get("endpoint")  #FIXME("현재 요청의 엔드포인트 함수?")
        if route and getattr(route, "_skip_jwt_verification", False):  # 데코레이터 확인??
            await self.app(scope, receive, send)
            return

        headers = Headers(scope=scope)
        try:
            token = self.extract_token(headers)
            payload = self.verify_token(token)
            scope["user"] = payload.get("sub")  # 사용자 정보를 scope에 저장
        except JWTError:
            response = JSONResponse({"detail": "Invalid or expired token"}, status_code=401)
            await response(scope, receive, send)
            return
        except Exception as e:
            response = JSONResponse({"detail": str(e)}, status_code=500)
            await response(scope, receive, send)
            return

        await self.app(scope, receive, send)

def skip_jwt_verification(func=None, *, condition=True):
    def decorator(func):
        func._skip_jwt_verification = condition
        return func
    return decorator if func is None else decorator(func)
