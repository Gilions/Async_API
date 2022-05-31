from typing import Optional

from elasticsearch import AsyncElasticsearch

es: Optional[AsyncElasticsearch] = None


# Подключаем Elastic
async def get_elastic() -> AsyncElasticsearch:
    return es
