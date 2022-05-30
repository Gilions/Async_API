from functools import lru_cache

from aioredis import Redis
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends

from db.elastic import get_elastic
from db.redis import get_redis
from models.movies import Genre
from services.base import BaseDitailService, BaseListService


class GenreService(BaseDitailService):
    model = Genre
    index = 'genres'


class GenresService(BaseListService):
    model = Genre
    index = 'genres'

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
        try:
            data = await self.elastic.search(index=self.index, body=query)
            response = [self.model(**row['_source']) for row in data['hits']['hits']]
        except NotFoundError:
            return None
        return response


@lru_cache()
def get_genre_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> GenreService:
    return GenreService(redis, elastic)


@lru_cache()
def get_genres_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> GenresService:
    return GenresService(redis, elastic)
