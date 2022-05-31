import logging
from typing import Iterator, List, Optional

from elasticsearch import Elasticsearch, helpers
from elasticsearch.exceptions import ConnectionError

from config import INDICES
from helpers import backoff


class ELKClient:
    """
       Класс загружает данные в ELK
       :param credentials - Параметры для подключения
       """
    def __init__(self, credentials: dict):
        self.client = None
        self.credentials = credentials
        self.indices = INDICES
        self.connect()

    @backoff()
    def connect(self):
        # Подключаемся к базе данных
        self.client = Elasticsearch(**self.credentials)

    def check_or_create_index(self, index: str):
        # Предварительная проверка, если индекс отсутствует в конфигурации, выходим
        # Если индекс есть в конфигурации, но не создан, создаем
        if index not in self.indices:
            logging.error('Конфигурация индекса отсутствует.')
            return

        for index_name, index in self.indices.items():
            if not self.client.indices.exists(index=index_name):
                self.client.indices.create(**index)

    @staticmethod
    def generate_data(data: Optional[list], index: str) -> Iterator[dict]:
        if not data:
            return

        for row in data:
            yield {
                '_index': index,
                '_id': row.uuid,
                '_source': row.json()
            }

    @backoff()
    def bulk_update(self, data: List, index: str):
        """
        Записываем данные в базу данных

        :param data: Данные для записи
        :param index: Индекс ELK
        """
        self.check_or_create_index(index=index)
        try:
            helpers.bulk(self.client, self.generate_data(data, index))
        except ConnectionError:
            logging.error('Отсутствует соединение с ELK')
            self.connect()
            helpers.bulk(self.client, self.generate_data(data, index))
