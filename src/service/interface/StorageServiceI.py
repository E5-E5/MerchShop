from abc import ABC, abstractmethod
from src.dto.api import InventoryItem


class StorageServiceI(ABC):

    @abstractmethod
    def get_list_of_storage(self, user_id: int) -> list[InventoryItem]:
        pass

    @abstractmethod
    def add_to_storage(self, user_id: int, merch: str):
        pass


