from functools import lru_cache
from typing import Optional, List


from aioredis import Redis
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends

from db.elastic import get_elastic
from db.redis import get_redis
from models.movies import Film
from orjson import loads

from services.utility import orjson_dumps

FILM_CACHE_EXPIRE_IN_SECONDS = 60 * 5


class FilmService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    async def get_by_id(self, film_id: str) -> Optional[Film]:
        film = await self._film_from_cache(film_id)
        if not film:
            film = await self._get_film_from_elastic(film_id)
            if not film:
                return None
            await self._put_film_to_cache(film)

        return film

    async def _get_film_from_elastic(self, film_id: str) -> Optional[Film]:
        try:
            doc = await self.elastic.get('movies', film_id)
        except NotFoundError:
            return None
        return Film(**doc['_source'])

    async def _film_from_cache(self, film_id: str) -> Optional[Film]:
        data = await self.redis.get(film_id)
        if not data:
            return None

        film = Film.parse_raw(data)
        return film

    async def _put_film_to_cache(self, film: Film):
        await self.redis.set(film.uuid, film.json(), expire=FILM_CACHE_EXPIRE_IN_SECONDS)


class FilmsService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    async def get_films(
            self,
            search: str = None,
            sorting: str = None,
            page_size: int = None,
            page_number: int = None):
        key = '{}/{}/{}/{}'.format(search, sorting, page_size, page_number)
        films = await self._films_from_cache(key=key)
        if not films:
            films = await self._get_films_from_elastic(page_size=page_size, page_number=page_number, sorting=sorting, search=search)
            if not films:
                return None
            await self._put_film_to_cache(key, films)
        return films

    async def _get_films_from_elastic(self, page_size, page_number, sorting: str = None, search: str = None):
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
            data = await self.elastic.search( index='movies', body=query)
            response = [Film(**film['_source']) for film in data['hits']['hits']]
        except NotFoundError:
            return None
        return response

    async def _films_from_cache(self, key: str):
        data = await self.redis.get(key)
        if not data:
            return None

        response = [Film.parse_raw(film) for film in loads(data)]
        return response

    async def _put_film_to_cache(self, key: str, films: List[Film]):
        await self.redis.set(
            key,
            orjson_dumps(films, default=Film.json),
            expire=FILM_CACHE_EXPIRE_IN_SECONDS
        )


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
