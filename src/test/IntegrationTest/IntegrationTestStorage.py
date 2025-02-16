import unittest
from src.storage.connector.PGConnector import PostgresDBConnector
from src.storage.implementation.StorageStorage import StorageStorage
from src.service.implementation.StorageService import StorageService
from src.dto.api import InventoryItem
from src.logger.Logger import Logger
from src.exception.Exception import *


class TestExchangeServiceIntegration(unittest.TestCase):
    logger: Logger
    connector: PostgresDBConnector
    storage_storage: StorageStorage
    storage_service: StorageService

    @classmethod
    def setUpClass(cls):
        cls.logger = Logger('../../logger/app_logs.log')
        cls.connector = PostgresDBConnector(cls.logger)
        cls.storage_storage = StorageStorage(cls.connector, cls.logger)
        cls.storage_service = StorageService(cls.connector, cls.storage_storage, cls.logger)
        cls.connector.connect()

        with cls.connector.connection as conn:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM cm.storage;")
                cursor.execute("DELETE FROM cm.user;")
                cursor.execute("DELETE FROM cm.merch;")

                cursor.execute("INSERT INTO cm.user (userid, FirstName, LastName, Gender, Coin, Login, Password)"
                               " VALUES (1, 'name1', 'last1', 'Male', 1000, 'login1', 'password1');")
                cursor.execute("INSERT INTO cm.user (userid, FirstName, LastName, Gender, Coin, Login, Password)"
                               " VALUES (2, 'name2', 'last2', 'Male', 10, 'login2', 'password2');")
                cursor.execute("""
                    INSERT INTO cm.Merch (MerchID, Name, Coin)
                    VALUES (1, 'Merch1', 100),
                           (2, 'Merch2', 150),
                           (3, 'Merch3', 200);
                """)
                cursor.execute("""
                    INSERT INTO cm.Storage (UserID, MerchID, Count)
                    VALUES (1, 1, 3);
                """)

                conn.commit()

    def test_get_storage(self):
        result = self.storage_service.get_list_of_storage(user_id=1)

        self.assertIsInstance(result[0], InventoryItem)
        self.assertEqual(result[0].quantity, 3)
        self.assertEqual(result[0].type, 'Merch1')

    def test_add_to_storage_old(self):
        self.storage_service.add_to_storage(user_id=1, merch='Merch3')
        self.storage_service.add_to_storage(user_id=1, merch='Merch3')

        with self.connector.connection as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT count FROM cm.storage WHERE UserID=1 AND MerchID=3;")
                new_transfer = cursor.fetchone()
                self.assertIsNotNone(new_transfer)
                self.assertEqual(new_transfer[0], 2)

    def test_add_to_storage_new(self):
        self.storage_service.add_to_storage(user_id=1, merch='Merch2')

        with self.connector.connection as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT count FROM cm.storage WHERE UserID=1 AND MerchID=2;")
                new_transfer = cursor.fetchone()
                self.assertIsNotNone(new_transfer)
                self.assertEqual(new_transfer[0], 1)

    def test_add_to_storage_non_merch(self):
        with self.assertRaises(MerchNotFoundException) as context:
            self.storage_service.add_to_storage(user_id=1, merch="Merch4")

        self.assertEqual(str(context.exception), "Мерч не найден")

    def test_add_to_storage_non_user(self):
        with self.assertRaises(UserNotFoundException) as context:
            self.storage_service.add_to_storage(user_id=5, merch="Merch4")

        self.assertEqual(str(context.exception), "Пользователь не найден")

    def test_add_to_storage_not_enough_coins(self):
        with self.assertRaises(NotEnoughCoinsException) as context:
            self.storage_service.add_to_storage(user_id=2, merch="Merch1")

        self.assertEqual(str(context.exception), "Недостаточно монет для операции")

    @classmethod
    def tearDownClass(cls):
        with cls.connector.connection as conn:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM cm.storage;")
                cursor.execute("DELETE FROM cm.user;")
                cursor.execute("DELETE FROM cm.merch;")
                conn.commit()


if __name__ == '__main__':
    unittest.main()
