from jinja2 import loaders
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from starlette.datastructures import Headers
from starlette.types import ASGIApp, Receive, Scope, Send
from jose import jwt, JWTError
from datetime import datetime
from core.config.config import loader

class VerifyTokenMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, secret_key: str, algorithm: str) -> None:
        super().__init__(app)
        self.secret_key = loader.config.SECRET_KEY
        self.algorithm = loader.config.ALGORITHM

    async def dispatch(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        headers = Headers(scope=scope)
        auth_header = headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            response = JSONResponse({"detail": "Authorization header missing or invalid"}, status_code=401)
            await response(scope, receive, send)
            return

        token = auth_header[len("Bearer "):]

        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            if payload.get("exp") < datetime.utcnow().timestamp():
                raise JWTError("Token has expired")
        except JWTError as e:
            response = JSONResponse({"detail": str(e)}, status_code=401)
            await response(scope, receive, send)
            return

        # Pass the request to the next middleware or endpoint
        await self.app(scope, receive, send)
