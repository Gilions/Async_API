from typing import List, Optional
from uuid import UUID

import orjson
from pydantic import BaseModel, Field

from services.utility import orjson_dumps


class ModelsMixim(BaseModel):
    uuid: UUID

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class Film(ModelsMixim):
    imdb_rating: Optional[float] = Field(default=0)
    title: str
    description: str = None
    genre: Optional[List]
    actors: Optional[List]
    writers: Optional[List]
    directors: Optional[List]


class Genre(ModelsMixim):
    name: str


class Person(ModelsMixim):
    full_name: str
    role: str
    film_ids: Optional[List]
