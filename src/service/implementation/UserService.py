from src.storage.connector.PGConnector import PostgresDBConnector
from ..interface.UserServiceI import UserServiceI
from src.storage.interface.UserStorageI import UserStorageI
from src.dto.user import UserRegistrationDTO
from src.model.user import User
from ..jwt.JWTAuth import JWTService
import hashlib
from src.logger.Logger import Logger


class UserService(UserServiceI):
    def __init__(self, connector: PostgresDBConnector, user_storage: UserStorageI,
                 jwt: JWTService, logger: Logger):
        self.connector = connector
        self.user_storage = user_storage
        self.jwt = jwt
        self.logger = logger

    def get_user_coin(self, user_id: int) -> int:
        return self.user_storage.get_user_coin(user_id)

    def hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    def register_user(self, user_registration: UserRegistrationDTO) -> User:
        hashed_password = self.hash_password(user_registration.password)
        user_registration.password = hashed_password
        result = self.user_storage.register_user(user_registration)
        return result if result else None

    def authenticate_user(self, login: str, password: str):
        hashed_password = self.hash_password(password)
        result = self.user_storage.authenticate_user(login, hashed_password)
        if not result:
            return None
        try:
            token = self.jwt.create_access_token(data={"sub": str(result.user_id)})
            return token
        except Exception as e:
            self.logger.error(f"Ошибка авторизации:{e}, login: {login}")
            raise e
