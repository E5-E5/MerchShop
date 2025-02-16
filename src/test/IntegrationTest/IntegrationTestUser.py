import unittest
from src.storage.connector.PGConnector import PostgresDBConnector
from src.storage.implementation.UserStorage import UserStorage
from src.service.implementation.UserService import UserService, UserRegistrationDTO
from src.model.user import Gender
from src.service.jwt.JWTAuth import JWTService
from src.exception.Exception import *
from src.logger.Logger import Logger


class TestExchangeServiceIntegration(unittest.TestCase):
    logger: Logger
    connector: PostgresDBConnector
    user_storage: UserStorage
    user_service: UserService
    jwt_service: JWTService

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

                cursor.execute("INSERT INTO cm.user (userid, FirstName, LastName, Gender, Coin, Login, Password)"
                               "VALUES (1, 'name1', 'last1', 'Male', 1000, 'login1', "
                               "'0b14d501a594442a01c6859541bcb3e8164d183d32937b851835442f69d5c94e');")

                conn.commit()

    def test_get_user_coin(self):
        result = self.user_service.get_user_coin(user_id=1)

        self.assertIsInstance(result, int)
        self.assertEqual(result, 1000)

    def test_get_coin_no_user(self):
        with self.assertRaises(NotCorrectRequestException) as context:
            self.user_service.get_user_coin(user_id=2)

        self.assertEqual(str(context.exception), "Некорректный запрос")

    def test_register_new_user(self):
        user_dto = UserRegistrationDTO(first_name='user2', last_name='last2',
                                       gender=Gender.MALE, login='login2', password='password2')
        result = self.user_service.register_user(user_dto)

        self.assertEqual(result[1:],
     ['user2', 'last2', 'Male', 1000, 'login2', '6cf615d5bcaac778352a8f1f3360d23f02f34ec182e259897fd6ce485d7870d4'])

    def test_register_new_user_bad_login(self):
        with self.assertRaises(NotCorrectRequestException) as context:
            user_dto = UserRegistrationDTO(first_name='user1', last_name='last1',
                                           gender=Gender.MALE, login='login1', password='password1')
            self.user_service.register_user(user_dto)

        self.assertEqual(str(context.exception), "Некорректный запрос")

    def test_authenticate_user(self):
        result = self.user_service.authenticate_user(login='login1', password='password1')
        self.assertIsNotNone(result)

    def test_authenticate_user_bad_password(self):
        with self.assertRaises(BadAuthenticateException) as context:
            self.user_service.authenticate_user(login='login1', password='password2')

        self.assertEqual(str(context.exception), "Неверный логин или пароль")

    @classmethod
    def tearDownClass(cls):
        with cls.connector.connection as conn:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM cm.user;")
                conn.commit()


if __name__ == '__main__':
    unittest.main()
