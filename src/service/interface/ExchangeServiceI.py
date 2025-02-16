from abc import ABC, abstractmethod
from src.dto.api import CoinHistory


class ExchangeServiceI(ABC):

    @abstractmethod
    def get_coin_history(self, user_id: int) -> CoinHistory:
        pass

    @abstractmethod
    def give_coins(self, user_id_from: int, user_login_to: str, coins: int):
        pass
