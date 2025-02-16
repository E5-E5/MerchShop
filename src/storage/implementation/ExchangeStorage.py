from ..interface.ExchangeStorageI import ExchangeStorageI, Exchange
from ..connector.PGConnector import PostgresDBConnector
from src.logger.Logger import Logger
from src.exception.Exception import *

class ExchangeStorage(ExchangeStorageI):
    def __init__(self, connector: PostgresDBConnector, logger: Logger):
        self.connector = connector
        self.logger = logger

    def get_list_received_coins(self, user_id: int) -> list[Exchange]:
        query = "SELECT * FROM cm.Exchange WHERE RecipientID = %s"
        result = self.connector.execute_query(query, [user_id], fetch=True)
        return result if result else []

    def get_list_send_coins(self, user_id: int) -> list[Exchange]:
        query = "SELECT * FROM cm.Exchange WHERE SenderID = %s"
        result = self.connector.execute_query(query, [user_id], fetch=True)
        return result if result else []

    def give_coins(self, user_id_from: int, user_login_to: str, coins: int):
        query_check_balance = "SELECT Coin FROM cm.User WHERE UserID = %s FOR UPDATE"
        query_get_id_to = "SELECT UserID FROM cm.User WHERE Login = %s"
        query_update_sender = "UPDATE cm.User SET Coin = Coin - %s WHERE UserID = %s"
        query_update_recipient = "UPDATE cm.User SET Coin = Coin + %s WHERE UserID = %s"
        query_insert_exchange = """
                    INSERT INTO cm.Exchange (SenderID, RecipientID, Coin, Date) 
                    VALUES (%s, %s, %s, CURRENT_TIMESTAMP)
                """

        try:
            with self.connector.connection as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query_check_balance, (user_id_from,))
                    sender_balance = cursor.fetchone()
                    if not sender_balance or sender_balance[0] < coins:
                        raise NotEnoughCoinsException()

                    cursor.execute(query_get_id_to, (user_login_to,))
                    user_id_to = cursor.fetchone()
                    if not user_id_to:
                        raise UserNotFoundException()

                    cursor.execute(query_update_sender, (coins, user_id_from))
                    cursor.execute(query_update_recipient, (coins, user_id_to))

                    cursor.execute(query_insert_exchange, (user_id_from, user_id_to, coins))

                conn.commit()
                return True

        except Exception as e:
            conn.rollback()
            self.logger.error(f"Ошибка при передачи монет: {e}, user_id_from: {user_id_from},"
                              f" user_login_to: {user_login_to}, coins: {coins}")
            raise e

