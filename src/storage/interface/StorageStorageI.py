from abc import ABC, abstractmethod
from src.model.storage import Storage
from src.dto.api import InventoryItem


class StorageStorageI(ABC):

    @abstractmethod
    def get_list_of_storage(self, user_id: int) -> list[list]:
        pass

    @abstractmethod
    def add_to_storage(self, user_id: int, merch: str):
        pass


