from ..interface.StorageStorageI import StorageStorageI
from ..connector.PGConnector import PostgresDBConnector
from src.dto.api import InventoryItem
from src.logger.Logger import Logger
from src.exception.Exception import *

class StorageStorage(StorageStorageI):
    def __init__(self, connector: PostgresDBConnector, logger: Logger):
        self.connector = connector
        self.logger = logger

    def get_list_of_storage(self, user_id: int) -> list[list]:
        query = """
                   SELECT m.Name, s.Count
                   FROM cm.Storage s
                   JOIN cm.Merch m ON s.MerchID = m.MerchID
                   WHERE s.UserID = %s
               """
        result = self.connector.execute_query(query, [user_id], fetch=True)
        return result if result else []

    def add_to_storage(self, user_id: int, merch: str):
        query_check_balance = "SELECT Coin FROM cm.User WHERE UserID = %s;"
        query_get_merch = "SELECT MerchID, Coin FROM cm.Merch WHERE Name = %s;"
        query_update_balance = "UPDATE cm.User SET Coin = Coin - %s WHERE UserID = %s;"
        query_add_to_storage = """
                    INSERT INTO cm.Storage (UserID, MerchID, Count)
                    VALUES (%s, %s, 1)
                    ON CONFLICT (UserID, MerchID) DO UPDATE
                    SET Count = cm.Storage.Count + 1;
                """

        try:
            with self.connector.connection as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query_check_balance, (user_id,))
                    user_coin = cursor.fetchone()
                    if not user_coin:
                        raise UserNotFoundException()
                    user_coin = user_coin[0]

                    cursor.execute(query_get_merch, (merch,))
                    merch_data = cursor.fetchone()
                    if not merch_data:
                        raise MerchNotFoundException()
                    merch_id = merch_data[0]
                    merch_price = merch_data[1]

                    if user_coin < merch_price:
                        raise NotEnoughCoinsException()

                    cursor.execute(query_update_balance, (merch_price, user_id))
                    cursor.execute(query_add_to_storage, (user_id, merch_id))

                    conn.commit()

        except Exception as e:
            conn.rollback()
            self.logger.error(f"Ошибка при покупке: {e}, user_id: {user_id},"
                              f" merch: {merch}")
            raise e


