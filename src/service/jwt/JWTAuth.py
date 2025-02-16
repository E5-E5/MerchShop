import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException
from src.exception.Exception import *

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class JWTService:
    def __init__(self, secret_key: str = SECRET_KEY, algorithm: str = ALGORITHM):
        self.secret_key = secret_key
        self.algorithm = algorithm

    def create_access_token(self, data: dict) -> str:
        try:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            to_encode = data.copy()
            to_encode.update({"exp": expire})
            token = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
            return token
        except Exception as e:
            raise JWTException()

    def validate_token(self, token: str) -> int:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])

            if datetime.utcnow() > datetime.utcfromtimestamp(payload['exp']):
                raise HTTPException(status_code=401, detail="Токен просрочен")

            return payload.get("sub")

        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Токен просрочен")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Неверный токен")
