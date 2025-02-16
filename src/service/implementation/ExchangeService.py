from src.service.interface.ExchangeServiceI import ExchangeServiceI
from src.storage.connector.PGConnector import PostgresDBConnector
from src.storage.implementation.ExchangeStorage import ExchangeStorageI
from src.storage.implementation.UserStorage import UserStorageI

from src.dto.api import CoinHistory
from src.logger.Logger import Logger
from datetime import datetime


class ExchangeService(ExchangeServiceI):
    def __init__(self, connector: PostgresDBConnector, exchange_storage: ExchangeStorageI,
                 user_storage: UserStorageI, logger: Logger):
        self.connector = connector
        self.exchange_storage = exchange_storage
        self.user_storage = user_storage
        self.logger = logger

    def convert_to_dict(self, data: list, type='from'):
        result = []

        if type == 'from':
            for i in data:
                login = self.user_storage.get_user_login(i[0])
                i_from = {'fromUser': login, 'amount': i[2], 'date': i[3].strftime('%d-%m-%Y')}
                result.append(i_from)
        else:
            for i in data:
                login = self.user_storage.get_user_login(i[1])
                i_to = {'toUser': login, 'amount': i[2], 'date': i[3].strftime('%d-%m-%Y')}
                result.append(i_to)

        return result

    def get_coin_history(self, user_id: int) -> CoinHistory:
        received = self.convert_to_dict(self.exchange_storage.get_list_received_coins(user_id))
        sent = self.convert_to_dict(self.exchange_storage.get_list_send_coins(user_id), type='to')

        result = CoinHistory(received=received, sent=sent)
        return result

    def give_coins(self, user_id_from: int, user_login_to: str, coins: int):
        self.exchange_storage.give_coins(user_id_from, user_login_to, coins)

