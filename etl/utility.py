import abc
from datetime import datetime
from typing import Any

from config import DSL, DSL_ELK, INDICES
from elk_client import ELKClient
from models import Genres, Movies
from pg_client import PGClient
from queryes import FW_SQL, GENRE_SQL, INSERT_ETL, SELECT_ETL


class BaseStorage:
    @abc.abstractmethod
    def save_state(self, query, data: dict) -> None:
        """Сохранить состояние в постоянное хранилище"""
        pass

    @abc.abstractmethod
    def retrieve_state(self, query, data: dict) -> datetime:
        """Загрузить состояние локально из постоянного хранилища"""
        pass


class PostgresStorage(BaseStorage):
    def __init__(self):
        self.client = PGClient(DSL)

    def save_state(self, data: dict, query=INSERT_ETL) -> None:
        self.client.insert(query, data)

    def retrieve_state(self, data: dict, query=SELECT_ETL) -> list:
        data = self.client.select(query, data)
        return data


class State:
    def __init__(self, storage=None):
        self.storage = storage if storage else PostgresStorage()
        self.start = None
        self.process = None

    def set_state(self) -> None:
        data = (dict(process=self.process, start=self.start))
        self.storage.save_state(data)

    def get_state(self, service: str) -> Any:
        self.start = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        self.process = service
        data = self.storage.retrieve_state(dict(process=service))
        if not data:
            return '{}'
        return data[0][0].strftime("%Y-%m-%d %H:%M:%S")


class UpdateElasticStorage:
    def __init__(self):
        self.elk_client = ELKClient(DSL_ELK)
        self.pg_client = PGClient(DSL)
        self.process = State()
        self.indices = INDICES

    @staticmethod
    def generate_data(data, models):
        rows = []
        for row in data:
            row = dict(row)
            rows.append(models(**row))
        return rows

    @staticmethod
    def _generate_query(sql: str, param: str, stage: str):
        if stage == '{}':
            sql = sql.format(param=True)
        else:
            param = param.format(date_time=stage)
            sql = sql.format(param=param)
        return sql

    def movies(self):
        param = """
            fw.modified > '{date_time}'
    OR
        fw.id in (
            SELECT pfw.film_work_id
            FROM person p
                INNER JOIN person_film_work pfw ON p.id = pfw.person_id
            WHERE p.modified > '{date_time}'
            )
    OR
        fw.id in (
            SELECT gfw.film_work_id
            FROM genre g
                INNER JOIN genre_film_work gfw ON g.id = gfw.genre_id
            WHERE g.modified > '{date_time}'
            )
        """
        stage = self.process.get_state('movies')
        sql = self._generate_query(sql=FW_SQL, param=param, stage=stage)
        data = self.generate_data(self.pg_client.select(sql), models=Movies)
        self.elk_client.bulk_update(data, 'movies')
        self.process.set_state()

    def genres(self):
        param = """modified > '{date_time}'"""
        stage = self.process.get_state('genres')
        sql = self._generate_query(sql=GENRE_SQL, param=param, stage=stage)
        data = self.generate_data(self.pg_client.select(sql), models=Genres)
        self.elk_client.bulk_update(data, 'genres')
        self.process.set_state()

    def run(self):
        for index in self.indices.keys():
            if index == 'movies':
                self.movies()
            elif index == 'genres':
                self.genres()
