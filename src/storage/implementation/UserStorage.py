from ..interface.UserStorageI import UserStorageI, User
from src.model.user import Gender
from ..connector.PGConnector import PostgresDBConnector
from src.dto.user import UserRegistrationDTO
from src.logger.Logger import Logger
from src.exception.Exception import *

class UserStorage(UserStorageI):
    def __init__(self, connector: PostgresDBConnector, logger: Logger):
        self.connector = connector
        self.logger = logger

    def get_user_login(self, user_id: int) -> str:
        query = """
                            Select Login from cm.User 
                            WHERE UserID = %s
                        """
        result = self.connector.execute_query(query, [user_id], fetch=True)

        if result:
            return result[0][0]
        self.logger.error(f"Ошибка при получении логина пользователя, user_id: {user_id}")
        raise NotCorrectRequestException()

    def get_user_coin(self, user_id: int) -> int:
        query = """
                    Select Coin from cm.User 
                    WHERE UserID = %s
                """
        result = self.connector.execute_query(query, [user_id], fetch=True)
        if result:
            return result[0][0]
        self.logger.error(f"Ошибка при получении монет пользователя, user_id: {user_id}")
        raise NotCorrectRequestException()

    def register_user(self, user_registration: UserRegistrationDTO) -> User:
        query = """
            INSERT INTO cm.User (FirstName, LastName, Gender, Login, Password, Coin)
            VALUES (%s, %s, %s, %s, %s, 1000)
            RETURNING *
        """
        result = self.connector.execute_query(query, [user_registration.first_name,
                                                      user_registration.last_name,
                                                      user_registration.gender.value,
                                                      user_registration.login,
                                                      user_registration.password], fetch=True)
        if result:
            return result[0]
        self.logger.error(f"Ошибка при регистрации пользователя, login: {user_registration.login}")
        raise NotCorrectRequestException()

    def authenticate_user(self, login: str, password: str) -> User:
        query = "SELECT * FROM cm.User WHERE Login = %s AND Password = %s"
        result = self.connector.execute_query(query, [login, password], fetch=True)
        if result:
            return User(
                user_id=result[0][0],
                first_name=result[0][1],
                last_name=result[0][2],
                gender=Gender[result[0][3].upper()],
                login=result[0][4],
                password=result[0][5],
                coin=result[0][6]
            )

        self.logger.error(f"Ошибка авторизации, login: {login}")
        raise BadAuthenticateException()

