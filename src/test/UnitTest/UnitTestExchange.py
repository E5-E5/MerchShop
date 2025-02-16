import unittest
from unittest.mock import MagicMock
from src.storage.connector.PGConnector import PostgresDBConnector
from src.storage.implementation.ExchangeStorage import ExchangeStorageI
from src.service.implementation.ExchangeService import ExchangeService
from src.storage.implementation.UserStorage import UserStorageI
from datetime import datetime

from src.logger.Logger import Logger
from src.exception.Exception import *


class TestExchangeService(unittest.TestCase):

    def setUp(self):
        self.mock_connector = MagicMock(spec=PostgresDBConnector)
        self.mock_exchange_storage = MagicMock(spec=ExchangeStorageI)
        self.mock_user_storage = MagicMock(spec=UserStorageI)
        self.mock_logger = MagicMock(spec=Logger)

        self.exchange_service = ExchangeService(self.mock_connector, self.mock_exchange_storage,
                                                self.mock_user_storage, self.mock_logger)

    def test_get_coin_history_success(self):
        mock_received = [[1, 2, 5, datetime.now()], [1, 3, 15, datetime.now()]]
        mock_sent = [[3, 1, 542, datetime.now()]]

        self.mock_exchange_storage.get_list_received_coins.return_value = mock_received
        self.mock_exchange_storage.get_list_send_coins.return_value = mock_sent

        result = self.exchange_service.get_coin_history(user_id=123)

        self.assertEqual(result.received[0].get('amount'), mock_received[0][2])
        self.assertEqual(result.sent[0].get('amount'), mock_sent[0][2])
        self.mock_exchange_storage.get_list_received_coins.assert_called_once_with(123)
        self.mock_exchange_storage.get_list_send_coins.assert_called_once_with(123)

    def test_get_coin_history_exception(self):
        self.mock_exchange_storage.get_list_received_coins.side_effect = ConnectionDBException()

        with self.assertRaises(ConnectionDBException) as context:
            self.exchange_service.get_coin_history(user_id=123)

        self.assertEqual(str(context.exception), "Не удалось подключиться к базе данных")

        self.mock_exchange_storage.get_list_received_coins.assert_called_once_with(123)

    def test_give_coins_success(self):
        self.exchange_service.give_coins(user_id_from=123, user_login_to="user456", coins=100)

        self.mock_exchange_storage.give_coins.assert_called_once_with(123, "user456", 100)

    def test_give_coins_no_user_to(self):
        self.mock_exchange_storage.give_coins.side_effect = UserNotFoundException()

        with self.assertRaises(UserNotFoundException) as context:
            self.exchange_service.give_coins(user_id_from=1, user_login_to="login5", coins=444)

        self.assertEqual(str(context.exception), "Пользователь не найден")
        self.mock_exchange_storage.give_coins.assert_called_once_with(1, "login5", 444)

    def test_give_coins_no_user_from(self):
        self.mock_exchange_storage.give_coins.side_effect = NotEnoughCoinsException()

        with self.assertRaises(NotEnoughCoinsException) as context:
            self.exchange_service.give_coins(user_id_from=5, user_login_to="login1", coins=444)

        self.assertEqual(str(context.exception), "Недостаточно монет для операции")
        self.mock_exchange_storage.give_coins.assert_called_once_with(5, "login1", 444)

    def test_give_coins_not_coins(self):
        self.mock_exchange_storage.give_coins.side_effect = NotEnoughCoinsException()

        with self.assertRaises(NotEnoughCoinsException) as context:
            self.exchange_service.give_coins(user_id_from=1, user_login_to="login2", coins=2000)

        self.assertEqual(str(context.exception), "Недостаточно монет для операции")
        self.mock_exchange_storage.give_coins.assert_called_once_with(1, "login2", 2000)


if __name__ == '__main__':
    unittest.main()