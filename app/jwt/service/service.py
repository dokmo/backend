from app.jwt.schemas.decoder import JWTDecoder
from app.jwt.schemas.encoder import JWTEncoder
from datetime import datetime
from zoneinfo import ZoneInfo


class JWTService:
    """
    JWT 로그인시 access token, refresh token을 생성하는 로직
    """

    def __init__(
            self,
            encoder: JWTEncoder,
            decoder: JWTDecoder,
            algorithm: str = None,
            secret_key: str = None,
            access_token_expire_time: int = None,
            refresh_token_expire_time: int = None,
    ):
        self.encoder = encoder
        self.decoder = decoder
        self.algorithm = algorithm
        self.secret_key = secret_key
        self.access_token_expire_time = access_token_expire_time
        self.refresh_token_expire_time = refresh_token_expire_time

    def create_access_token(self, data: dict) -> str:
        return self._create_token(data, self.access_token_expire_time)

    def create_refresh_token(self, data: dict) -> str:
        return self._create_token(data, self.refresh_token_expire_time)

    def _create_token(self, data: dict, expires_delta: int) -> str:
        return self.encoder.encode(data, expires_delta, self.secret_key, self.algorithm)

    def check_token_expired(self, token: str) -> dict | None:
        payload = self.decoder.decode(token, self.secret_key, self.algorithm)

        now = datetime.timestamp(datetime.now(ZoneInfo("Asia/Seoul")))
        if payload and payload["exp"] < now:
            return None

        return payload