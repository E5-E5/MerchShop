import unittest
from unittest.mock import MagicMock
from src.service.implementation.StorageService import StorageService
from src.storage.connector.PGConnector import PostgresDBConnector
from src.storage.interface.StorageStorageI import StorageStorageI
from src.logger.Logger import Logger
from src.dto.api import InventoryItem
from src.exception.Exception import *


class TestStorageService(unittest.TestCase):

    def setUp(self):
        self.mock_connector = MagicMock(spec=PostgresDBConnector)
        self.mock_storage = MagicMock(spec=StorageStorageI)
        self.mock_logger = MagicMock(spec=Logger)

        self.storage_service = StorageService(self.mock_connector, self.mock_storage, self.mock_logger)

    def test_get_list_of_storage_success(self):
        mock_items = [["item1", 3],
                      ["item2", 2]]
        self.mock_storage.get_list_of_storage.return_value = mock_items

        result = self.storage_service.get_list_of_storage(user_id=123)
        self.assertEqual(result, [InventoryItem(type='item1', quantity=3),
                                  InventoryItem(type='item2', quantity=2)])
        self.mock_storage.get_list_of_storage.assert_called_once_with(123)

    def test_get_list_of_storage_exception(self):
        mock_items = []
        self.mock_storage.get_list_of_storage.return_value = mock_items

        result = self.storage_service.get_list_of_storage(user_id=123)

        self.assertEqual(result, mock_items)
        self.mock_storage.get_list_of_storage.assert_called_once_with(123)

    def test_add_to_storage_success(self):
        self.storage_service.add_to_storage(user_id=123, merch="NewItem")

        self.mock_storage.add_to_storage.assert_called_once_with(123, "NewItem")

    def test_add_to_storage_non_merch(self):
        self.mock_storage.add_to_storage.side_effect = MerchNotFoundException()

        with self.assertRaises(MerchNotFoundException) as context:
            self.storage_service.add_to_storage(user_id=1, merch="Merch4")

        self.assertEqual(str(context.exception), "Мерч не найден")
        self.mock_storage.add_to_storage.assert_called_once_with(1, "Merch4")

    def test_add_to_storage_non_user(self):
        self.mock_storage.add_to_storage.side_effect = UserNotFoundException()

        with self.assertRaises(UserNotFoundException) as context:
            self.storage_service.add_to_storage(user_id=5, merch="Merch4")

        self.assertEqual(str(context.exception), "Пользователь не найден")
        self.mock_storage.add_to_storage.assert_called_once_with(5, "Merch4")

    def test_add_to_storage_not_enough_coins(self):
        self.mock_storage.add_to_storage.side_effect = NotEnoughCoinsException()

        with self.assertRaises(NotEnoughCoinsException) as context:
            self.storage_service.add_to_storage(user_id=2, merch="Merch1")

        self.assertEqual(str(context.exception), "Недостаточно монет для операции")
        self.mock_storage.add_to_storage.assert_called_once_with(2, "Merch1")


if __name__ == '__main__':
    unittest.main()
