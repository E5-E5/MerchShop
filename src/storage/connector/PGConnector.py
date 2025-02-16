import psycopg2
from psycopg2.extras import DictCursor
from typing import Any, List, Optional
from src.logger.Logger import Logger
from src.storage.connector.config_bd import *
from src.exception.Exception import *


class PostgresDBConnector:
    def __init__(self, logger: Logger):
        self.database = database
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.connection = None

        self.logger = logger

    def connect(self):
        if not self.connection:
            try:
                self.connection = psycopg2.connect(
                    database=self.database,
                    user=self.user,
                    password=self.password,
                    host=self.host,
                    port=self.port
                )
                self.logger.info("Успешное подключение к базе данных")
            except psycopg2.Error as e:
                self.logger.error(f"Ошибка подключения к базе данных: {e}")
                raise ConnectionDBException()
            except Exception as e:
                self.logger.critical(f"Неизвестная ошибка: {e}")
                raise e

    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None
            self.logger.info("Соединение с базой данных закрыто")

    def execute_query(self, query: str, params: Optional[List[Any]] = None, fetch: bool = False):
        if not self.connection:
            self.connect()

        try:
            with self.connection.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(query, params)
                if fetch:
                    self.connection.commit()
                    return cursor.fetchall()
        except psycopg2.Error as e:
            self.logger.error(f"Ошибка выполнения запроса: {e}")
            self.connection.rollback()
            raise NotCorrectRequestException()
