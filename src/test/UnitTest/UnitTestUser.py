import unittest
from unittest.mock import MagicMock
from src.storage.connector.PGConnector import PostgresDBConnector
from src.storage.implementation.UserStorage import UserStorageI
from src.service.implementation.UserService import UserService, UserRegistrationDTO
from src.service.jwt.JWTAuth import JWTService
from src.model.user import Gender

from src.logger.Logger import Logger
from src.exception.Exception import *


class TestExchangeService(unittest.TestCase):

    def setUp(self):
        self.mock_connector = MagicMock(spec=PostgresDBConnector)
        self.mock_user_storage = MagicMock(spec=UserStorageI)
        self.mock_logger = MagicMock(spec=Logger)
        self.mock_jwt = MagicMock(spec=JWTService)
        self.user_service = UserService(self.mock_connector, self.mock_user_storage, self.mock_jwt, self.mock_logger)

    def test_get_user_coin_success(self):
        mock_coin = 10

        self.mock_user_storage.get_user_coin.return_value = mock_coin

        result = self.user_service.get_user_coin(user_id=123)

        self.assertEqual(result, mock_coin)
        self.mock_user_storage.get_user_coin.assert_called_once_with(123)

    def test_get_user_coin_no_user(self):
        self.mock_user_storage.get_user_coin.side_effect = NotCorrectRequestException()

        with self.assertRaises(NotCorrectRequestException) as context:
            self.user_service.get_user_coin(user_id=123)

        self.assertEqual(str(context.exception), "Некорректный запрос")
        self.mock_user_storage.get_user_coin.assert_called_once_with(123)

    def test_register_new_user(self):
        user_dto = UserRegistrationDTO(first_name='user2', last_name='last2', gender=Gender.MALE, login='login2', password='password2')

        mock_user = ['user2', 'last2', 'Male', 'login2', 'password2']
        self.mock_user_storage.register_user.return_value = mock_user

        result = self.user_service.register_user(user_dto)
        self.assertEqual(result, mock_user)

    def test_register_new_user_bad_login(self):
        user_dto = UserRegistrationDTO(
            first_name='user1',
            last_name='last1',
            gender=Gender.MALE,
            login='login1',
            password='password1'
        )

        self.mock_user_storage.register_user.side_effect = NotCorrectRequestException()

        with self.assertRaises(NotCorrectRequestException) as context:
            self.user_service.register_user(user_dto)

        self.assertEqual(str(context.exception), "Некорректный запрос")

if __name__ == '__main__':
    unittest.main()