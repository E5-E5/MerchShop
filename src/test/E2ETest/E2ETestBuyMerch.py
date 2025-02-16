import unittest
from src.storage.connector.PGConnector import PostgresDBConnector
from src.storage.implementation.UserStorage import UserStorage
from src.service.implementation.UserService import UserService
from src.service.jwt.JWTAuth import JWTService
import requests

from src.logger.Logger import Logger


class TestBuyMerch(unittest.TestCase):
    logger: Logger
    connector: PostgresDBConnector
    user_storage: UserStorage
    user_service: UserService
    jwt_service: JWTService

    BASE_URL = "http://localhost:8080"

    @classmethod
    def setUpClass(cls):
        cls.logger = Logger('../../logger/app_logs.log')
        cls.connector = PostgresDBConnector(cls.logger)
        cls.jwt_service = JWTService()
        cls.user_storage = UserStorage(cls.connector, cls.logger)
        cls.user_service = UserService(cls.connector, cls.user_storage, cls.jwt_service, cls.logger)
        cls.connector.connect()

        with cls.connector.connection as conn:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM cm.user;")
                cursor.execute("DELETE FROM cm.merch;")

                cursor.execute("INSERT INTO cm.user (userid, FirstName, LastName, Gender, Coin, Login, Password)"
                               "VALUES (1, 'name1', 'last1', 'Male', 5000, 'login1', "
                               "'0b14d501a594442a01c6859541bcb3e8164d183d32937b851835442f69d5c94e');")
                cursor.execute("""
                                    INSERT INTO cm.Merch (MerchID, Name, Coin)
                                    VALUES (1, 'Merch1', 100),
                                           (2, 'Merch2', 150),
                                           (3, 'Merch3', 900);
                                """)
                conn.commit()

    def test_buy_merch(self):
        auth_data = {
            "username": "login1",
            "password": "password1"
        }
        response = requests.post(f"{self.BASE_URL}/api/auth", json=auth_data)
        assert response.status_code == 200
        data = response.json()
        assert "token" in data
        token = data["token"]
        self.token = token

        headers = {"Authorization": f"Bearer {self.token}"}

        response = requests.get(f"{self.BASE_URL}/api/info", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert "coins" in data
        assert "inventory" in data

        merch_name_1 = "Merch1"
        merch_name_2 = "Merch2"

        response = requests.get(f"{self.BASE_URL}/api/buy/{merch_name_1}", headers=headers)
        assert response.status_code == 200
        assert response.json()["message"] == f"Предмет '{merch_name_1}' успешно куплен"

        response = requests.get(f"{self.BASE_URL}/api/info", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert "coins" in data
        assert "inventory" in data

        response = requests.get(f"{self.BASE_URL}/api/buy/{merch_name_1}", headers=headers)
        assert response.status_code == 200

        response = requests.get(f"{self.BASE_URL}/api/buy/{merch_name_2}", headers=headers)
        assert response.status_code == 200

        response = requests.get(f"{self.BASE_URL}/api/info", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert "coins" in data
        assert "inventory" in data

    @classmethod
    def tearDownClass(cls):
        with cls.connector.connection as conn:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM cm.user;")
                cursor.execute("DELETE FROM cm.merch;")
                conn.commit()

