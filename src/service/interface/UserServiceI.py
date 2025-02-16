from abc import ABC, abstractmethod
from src.model.user import User
from src.dto.user import UserRegistrationDTO


class UserServiceI(ABC):

    @abstractmethod
    def get_user_coin(self, user_id: int) -> int:
        pass

    @abstractmethod
    def register_user(self, user_registration: UserRegistrationDTO) -> User:
        pass

    @abstractmethod
    def authenticate_user(self, login: str, password: str):
        pass

