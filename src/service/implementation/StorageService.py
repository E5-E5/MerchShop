from ..interface.StorageServiceI import StorageServiceI
from src.storage.implementation.StorageStorage import StorageStorageI
from src.storage.connector.PGConnector import PostgresDBConnector
from src.dto.api import InventoryItem
from src.logger.Logger import Logger


class StorageService(StorageServiceI):
    def __init__(self, connector: PostgresDBConnector, storage_storage: StorageStorageI, logger: Logger):
        self.connector = connector
        self.storage_storage = storage_storage
        self.logger = logger

    def get_list_of_storage(self, user_id: int) -> list[InventoryItem]:
        storage = self.storage_storage.get_list_of_storage(user_id)
        return [InventoryItem(type=item[0], quantity=item[1]) for item in storage]

    def add_to_storage(self, user_id: int, merch: str):
        self.storage_storage.add_to_storage(user_id, merch)


