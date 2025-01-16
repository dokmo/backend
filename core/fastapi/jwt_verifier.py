from fastapi import HTTPException
from jose import JWTError
from starlette.requests import Request

from app.jwt.decoder import AbstractJWTDecoder, JWTDecoder

decoder: AbstractJWTDecoder = JWTDecoder()

# def authorization_jwt(func: Callable):
#     @wraps(func)
#     async def wrapper(*args, **kwargs ):
#         request: Request = kwargs.get("request")
#         if not request:
#             raise HTTPException(status_code=400, detail="Request object is required")
#
#         auth_header = request.headers.get("Authorization")
#         if not auth_header or not auth_header.startswith("Bearer "):
#             raise HTTPException(status_code=401, detail="Authorization header missing or invalid")
#
#         token = auth_header[len("Bearer "):]
#         try:
#             payload = decoder.decode(token=token)
#             print(payload)
#             kwargs["user_id"] = payload.get("user_id", None)
#         except JWTError as e:
#             raise HTTPException(status_code=401, detail=f"Invalid or expired token: {str(e)}")
#
#         return await func(*args, **kwargs)
#
#     return wrapper


async def require_authorization(request: Request):
    """
    This asynchronous function validates the presence and structure of an authorization
    header in a request. It ensures the header contains a valid Bearer token, decodes
    the token, and extracts the user ID if present. If the authorization header is
    absent, malformed, or the token is invalid or expired, an HTTPException with a
    401 status code is raised.

    :param request: The HTTP request object containing headers with an
        Authorization field.
    :type request: Request
    :return: The extracted user ID if the token is valid, otherwise raises an
        HTTPException.
    :rtype: Optional[str]
    :raises HTTPException: If the Authorization header is missing, malformed,
        or the token is invalid or expired.
    """
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authorization header missing or invalid")

    token = auth_header[len("Bearer "):]
    try:
        payload = decoder.decode(token=token)
        return payload.get("user_id", None)
    except JWTError as e:
        raise HTTPException(status_code=401, detail=f"Invalid or expired token: {str(e)}")


async def try_validate_token (request: Request):
    """
    Validates a JWT token from the authorization header of an incoming request.

    This function extracts the "Authorization" header from the request, checks if
    it follows the "Bearer <token>" pattern, and decodes the token using the
    configured decoder. If the token is valid, it extracts the "user_id" from the
    token payload. If the header is missing, incorrectly formatted, or the token
    is invalid, it returns None. This ensures secure and authenticated access
    to resources requiring token verification.

    :param request: The HTTP request object containing headers.
    :type request: Request

    :return: The user ID extracted from the decoded token if valid, otherwise None.
    :rtype: Optional[Any]
    """
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return None

    token = auth_header[len("Bearer "):]
    try:
        payload = decoder.decode(token=token)
        return payload.get("user_id", None)
    except JWTError as e:
        return None