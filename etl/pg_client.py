import logging

import psycopg2
from psycopg2.extras import DictCursor

from helpers import backoff


class PGClient:
    """
    Класс работает с базой данных Postgres
    :param credentials - Параметры для подключения
    :param chunk - Размер доставаемых данных
    """
    def __init__(self, credentials: dict, chunk=500):
        self.db_connect = None
        self.cursor = None
        self.credentials = credentials
        self.chunk = chunk

    @backoff()
    def connection(self):
        # Подключаемся к базе данных
        self.db_connect = psycopg2.connect(**self.credentials, cursor_factory=DictCursor)
        self.cursor = self.db_connect.cursor()

    @backoff()
    def _make_request(self, sql: str):
        # Производим запрос в базу данных, в случаи ошибки соединения, повторим запрос
        try:
            self.connection()
            self.cursor.execute(sql)
        except psycopg2.OperationalError:
            logging.error('Возникла ошибки при подключении к базе данных.')
            self.connection()
            self.cursor.execute(sql)

    def insert(self, sql: str, data: dict):
        # Производит запись данных в БД
        sql = sql.format(**data)
        self._make_request(sql)
        self.db_connect.commit()
        self.cursor.close()

    def select(self, sql: str, data: dict = None) -> list:
        # Получает данные из БД
        if data:
            sql = sql.format(**data)
        self._make_request(sql)
        data = []
        rows = self.cursor.fetchmany(self.chunk)
        while rows:
            for row in rows:
                data.append(row)
            rows = self.cursor.fetchmany(self.chunk)
        self.cursor.close()
        return data
