from functools import lru_cache

from aioredis import Redis
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends

from db.elastic import get_elastic
from db.redis import get_redis
from models.movies import Film
from services.base import BaseDitailService, BaseListService


class FilmService(BaseDitailService):
    model = Film
    index = 'movies'


class FilmsService(BaseListService):
    model = Film
    index = 'movies'

    async def _get_from_elastic(
            self,
            page_size,
            page_number,
            sorting: str = None,
            search: str = None):
        query = {
            "size": page_size,
            "from": (page_number - 1) * page_size,
            "query": {"match_all": {}}
        }
        if sorting:
            method = 'desc' if sorting == '-imdb_rating' else 'asc'
            query['sort'] = [dict(imdb_rating=method)]
        elif search:
            query['query'] = {
                'simple_query_string': {
                    'query': search,
                    'fields': ['title^3', 'description'],
                    'default_operator': 'or'
                }
            }
        try:
            data = await self.elastic.search(index=self.index, body=query)
            response = [self.model(**row['_source']) for row in data['hits']['hits']]
        except NotFoundError:
            return None
        return response


@lru_cache()
def get_film_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    return FilmService(redis, elastic)


@lru_cache()
def get_films_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmsService:
    return FilmsService(redis, elastic)
