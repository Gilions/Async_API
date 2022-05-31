from functools import lru_cache

from aioredis import Redis
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends

from db.elastic import get_elastic
from db.redis import get_redis
from models.movies import Person
from services.base import BaseDitailService, BaseListService


class PersonService(BaseDitailService):
    model = Person
    index = 'persons'


class PersonsService(BaseListService):
    model = Person
    index = 'persons'

    async def _get_from_elastic(
            self,
            page_size,
            page_number,
            sorting: str = None,
            search: str = None):
        query = {
            "size": page_size,
            "from": (page_number - 1) * page_size,
            'query': {
                'simple_query_string': {
                    'query': search,
                    'fields': ['uuid', 'full_name^3', 'role'],
                    'default_operator': 'or'
                }
            }
        }
        try:
            data = await self.elastic.search(index=self.index, body=query)
            response = [self.model(**row['_source']) for row in data['hits']['hits']]
        except NotFoundError:
            return None
        return response


@lru_cache()
def get_person_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> PersonService:
    return PersonService(redis, elastic)


@lru_cache()
def get_persons_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> PersonsService:
    return PersonsService(redis, elastic)
