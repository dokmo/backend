from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from starlette.types import ASGIApp
from jose import jwt, JWTError
from core.config.config import loader

class VerifyTokenMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp) -> None:
        super().__init__(app)
        self.secret_key = loader.config.SECRET_KEY
        self.algorithm = loader.config.ALGORITHM

    def extract_token(self, headers) -> str:
        auth_header = headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise JWTError("Authorization header missing or invalid")
        return auth_header[len("Bearer "):]

    def verify_token(self, token: str) -> dict:
        return jwt.decode(token, self.secret_key, algorithms=[self.algorithm], options={"verify_exp": True})

    async def dispatch(self, request: Request, call_next):
        headers = request.headers
        try:
            token = self.extract_token(headers)
            payload = self.verify_token(token)
            request.scope["user_id"] = payload.get("user_id", None)
        except JWTError:
            return JSONResponse({"detail": "Invalid or expired token"}, status_code=401)
        except Exception as e:
            return JSONResponse({"detail": str(e)}, status_code=500)

        return await call_next(request)