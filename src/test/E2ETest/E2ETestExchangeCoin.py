import unittest
from src.storage.connector.PGConnector import PostgresDBConnector
from src.storage.implementation.UserStorage import UserStorage
from src.service.implementation.UserService import UserService
from src.service.jwt.JWTAuth import JWTService
import requests

from src.logger.Logger import Logger


class E2ETestExchangeCoin(unittest.TestCase):
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
                cursor.execute("DELETE FROM cm.exchange;")

                cursor.execute("INSERT INTO cm.user (userid, FirstName, LastName, Gender, Coin, Login, Password)"
                               "VALUES (1, 'name1', 'last1', 'Male', 1000, 'login1', "
                               "'0b14d501a594442a01c6859541bcb3e8164d183d32937b851835442f69d5c94e');")
                cursor.execute("INSERT INTO cm.user (userid, FirstName, LastName, Gender, Coin, Login, Password)"
                               "VALUES (2, 'name2', 'last2', 'Male', 1000, 'login2', "
                               "'0b14d501a594442a01c6859541bcb3e8164d183d32937b851835442f69d5c94e');")

                conn.commit()

    def test_exchange_coin(self):
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

        request_data = {
            "toUser": "login2",
            "amount": 50
        }
        response = requests.post(f"{self.BASE_URL}/api/sendCoin", json=request_data, headers=headers)

        assert response.status_code == 200  # Успешный ответ
        assert response.json()["message"] == "Монеты успешно отправлены"

        response = requests.get(f"{self.BASE_URL}/api/info", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert "coins" in data
        assert "inventory" in data

        request_data = {
            "toUser": "login1",
            "amount": 900
        }
        response = requests.post(f"{self.BASE_URL}/api/sendCoin", json=request_data, headers=headers)

        assert response.status_code == 200
        assert response.json()["message"] == "Монеты успешно отправлены"

    @classmethod
    def tearDownClass(cls):
        with cls.connector.connection as conn:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM cm.user;")
                cursor.execute("DELETE FROM cm.exchange;")
                conn.commit()

