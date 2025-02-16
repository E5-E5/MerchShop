from abc import ABC, abstractmethod
from src.model.exchange import Exchange


class ExchangeStorageI(ABC):

    @abstractmethod
    def get_list_received_coins(self, user_id: int) -> list[Exchange]:
        pass

    @abstractmethod
    def get_list_send_coins(self, user_id: int) -> list[Exchange]:
        pass

    @abstractmethod
    def give_coins(self, user_id_from: int, user_login_to: str, coins: int):
        pass

