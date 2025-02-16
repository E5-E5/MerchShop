from abc import ABC, abstractmethod
from typing import List
from src.model.user import User
from src.model.merch import Merch
from src.dto.user import UserRegistrationDTO


class UserStorageI(ABC):
    @abstractmethod
    def get_user_login(self, user_id: int) -> str:
        pass

    @abstractmethod
    def get_user_coin(self, user_id: int) -> int:
        pass

    @abstractmethod
    def register_user(self, user_registration: UserRegistrationDTO) -> User:
        pass

    @abstractmethod
    def authenticate_user(self, login: str, password: str) -> User:
        pass
