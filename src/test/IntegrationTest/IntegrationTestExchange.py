import unittest
from src.storage.connector.PGConnector import PostgresDBConnector
from src.storage.implementation.ExchangeStorage import ExchangeStorage
from src.storage.implementation.UserStorage import UserStorage
from src.service.implementation.ExchangeService import ExchangeService
from src.dto.api import CoinHistory
from src.logger.Logger import Logger
from src.exception.Exception import *


class TestExchangeServiceIntegration(unittest.TestCase):
    logger: Logger
    connector: PostgresDBConnector
    exchange_storage: ExchangeStorage
    user_storage: UserStorage
    exchange_service: ExchangeService

    @classmethod
    def setUpClass(cls):
        cls.logger = Logger('../../logger/app_logs.log')
        cls.connector = PostgresDBConnector(cls.logger)
        cls.exchange_storage = ExchangeStorage(cls.connector, cls.logger)
        cls.user_storage = UserStorage(cls.connector, cls.logger)
        cls.exchange_service = ExchangeService(cls.connector, cls.exchange_storage, cls.user_storage, cls.logger)
        cls.connector.connect()
        with cls.connector.connection as conn:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM cm.exchange;")
                cursor.execute("DELETE FROM cm.user;")

                cursor.execute("INSERT INTO cm.user (userid, FirstName, LastName, Gender, Coin, Login, Password)"
                               " VALUES (1, 'name1', 'last1', 'Male', 1000, 'login1', 'password1');")
                cursor.execute("INSERT INTO cm.user (userid, FirstName, LastName, Gender, Coin, Login, Password)"
                               " VALUES (2, 'name2', 'last2', 'Male', 1000, 'login2', 'password2');")
                cursor.execute("INSERT INTO cm.exchange (SenderID, RecipientID, Coin) VALUES (1, 2, 111);")

                conn.commit()

    def test_get_coin_history_part(self):
        result = self.exchange_service.get_coin_history(user_id=1)
        self.assertIsInstance(result, CoinHistory)
        self.assertEqual(len(result.sent), 1)
        self.assertEqual(result.sent[0]["amount"], 111)

    def test_give_coins(self):
        self.exchange_service.give_coins(user_id_from=2, user_login_to="login1", coins=444)

        with self.connector.connection as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT coin FROM cm.exchange WHERE SenderID=2 AND RecipientID=1;")
                new_transfer = cursor.fetchone()
                self.assertIsNotNone(new_transfer)
                self.assertEqual(new_transfer[0], 444)

    def test_get_coin_history_all(self):
        self.exchange_service.give_coins(user_id_from=2, user_login_to="login1", coins=444)

        result = self.exchange_service.get_coin_history(user_id=1)
        self.assertIsInstance(result, CoinHistory)
        self.assertEqual(len(result.sent), 1)
        self.assertEqual(result.received[0]["amount"], 444)

    def test_give_coins_no_user_to(self):
        with self.assertRaises(UserNotFoundException) as context:
            self.exchange_service.give_coins(user_id_from=1, user_login_to="login5", coins=444)

        self.assertEqual(str(context.exception), "Пользователь не найден")

    def test_give_coins_no_user_from(self):
        with self.assertRaises(NotEnoughCoinsException) as context:
            self.exchange_service.give_coins(user_id_from=5, user_login_to="login1", coins=444)

        self.assertEqual(str(context.exception), "Недостаточно монет для операции")

    def test_give_coins_not_coins(self):
        with self.assertRaises(NotEnoughCoinsException) as context:
            self.exchange_service.give_coins(user_id_from=1, user_login_to="login2", coins=2000)

        self.assertEqual(str(context.exception), "Недостаточно монет для операции")

    @classmethod
    def tearDownClass(cls):
        with cls.connector.connection as conn:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM cm.exchange;")
                cursor.execute("DELETE FROM cm.user;")
                conn.commit()


if __name__ == '__main__':
    unittest.main()
