import abc
import logging
from typing import List, Optional, Union
from uuid import UUID

from aioredis import Redis
from elasticsearch import AsyncElasticsearch, NotFoundError
from orjson import loads

from core.config import CACHE_EXPIRE_IN_SECONDS
from models.movies import Film, Genre, Person
from services.utility import orjson_dumps

logger = logging.getLogger(__name__)


class BaseDitailService:
    """
    Базовый клас, используется для вывода конкретного инстанса.
    :param redis - Редис, используется для кеширования данных.
    :param elastic - Основная БД
    """
    model = None
    index = None

    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

        if not self.model or not self.index:
            logging.error('Необходимо указать модель и индекс')
            raise ValueError('Необходимо указать модель и индекс')

    async def get_by_uuid(self, uuid: UUID) -> Optional[Union[Film, Genre, Person]]:
        # Используется следующая логика:
        # Проверяем кеш, если нет идем в БД, полученные данные кешируем на 5 минут.
        data = await self._get_from_cache(uuid)
        if not data:
            data = await self._get_from_elastic(uuid)
            if not data:
                return None
            await self._put_to_cache(data)
        return data

    async def _get_from_elastic(self, uuid: UUID) -> Optional[Union[Film, Genre, Person]]:
        try:
            doc = await self.elastic.get(self.index, uuid)
        except NotFoundError:
            return None
        return self.model(**doc['_source'])

    async def _get_from_cache(self, uuid: UUID) -> Optional[Union[Film, Genre, Person]]:
        data = await self.redis.get(str(uuid))
        if not data:
            return None
        return self.model.parse_raw(data)

    async def _put_to_cache(self, data: Union[Film, Genre, Person]):
        await self.redis.set(str(data.uuid), data.json(), expire=CACHE_EXPIRE_IN_SECONDS)


class BaseListService:
    """
        Базовый клас, используется для вывода списка инстансов.
        :param redis - Редис, используется для кеширования данных.
        :param elastic - Основная БД
        """
    model = None
    index = None

    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

        if not self.model or not self.index:
            logging.error('Необходимо указать модель и индекс')
            raise ValueError('Необходимо указать модель и индекс')

    async def get_data(
            self,
            search: str = None,
            sorting: str = None,
            page_size: int = None,
            page_number: int = None):
        # Используется следующая логика:
        # Проверяем кеш, если нет идем в БД, полученные данные кешируем на 5 минут.
        key = '{}/{}/{}/{}/{}'.format(self.index, search, sorting, page_size, page_number)
        data = await self._get_from_cache(key=key)
        if not data:
            data = await self._get_from_elastic(
                page_size=page_size,
                page_number=page_number,
                sorting=sorting,
                search=search)
            if not data:
                return None
            await self._put_to_cache(key, data)
        return data

    @abc.abstractmethod
    async def _get_from_elastic(
            self,
            page_size: int,
            page_number: int,
            sorting: str = None,
            search: str = None) -> Optional[List[Union[Film, Genre, Person]]]:
        pass

    async def _get_from_cache(self, key: str) -> Optional[List[Union[Film, Genre, Person]]]:
        data = await self.redis.get(key)
        if not data:
            return None
        response = [self.model.parse_raw(row) for row in loads(data)]
        return response

    async def _put_to_cache(self, key: str, data: List[Union[Film, Genre, Person]]):
        await self.redis.set(
            key,
            orjson_dumps(data, default=Film.json),
            expire=CACHE_EXPIRE_IN_SECONDS
        )
