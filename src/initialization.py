from src.storage.connector.PGConnector import PostgresDBConnector
from src.service.jwt.JWTAuth import JWTService
from src.logger.Logger import Logger

from src.storage.implementation.UserStorage import UserStorage, UserStorageI
from src.storage.implementation.StorageStorage import StorageStorage, StorageStorageI
from src.storage.implementation.ExchangeStorage import ExchangeStorage, ExchangeStorageI

from src.service.implementation.UserService import UserService, UserServiceI
from src.service.implementation.StorageService import StorageService, StorageServiceI
from src.service.implementation.ExchangeService import ExchangeService, ExchangeServiceI

logger = Logger()
connector = PostgresDBConnector(logger)
jwt_service = JWTService()

user_storage: UserStorageI = UserStorage(connector, logger)
storage_storage: StorageStorageI = StorageStorage(connector, logger)
exchange_storage: ExchangeStorageI = ExchangeStorage(connector, logger)

user_service: UserServiceI = UserService(connector, user_storage, jwt_service, logger)
storage_service: StorageServiceI = StorageService(connector, storage_storage, logger)
exchange_service: ExchangeServiceI = ExchangeService(connector, exchange_storage, user_storage, logger)


def get_jwt_service() -> JWTService:
    return jwt_service


def get_user_service() -> UserServiceI:
    return user_service


def get_storage_service() -> StorageServiceI:
    return storage_service


def get_exchange_service() -> ExchangeServiceI:
    return exchange_service
