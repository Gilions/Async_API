from typing import Optional, List

import orjson

from pydantic import BaseModel, Field

from services.utility import orjson_dumps


class Film(BaseModel):
    uuid: str
    imdb_rating: Optional[float] = Field(default=0)
    title: str
    description: str = None
    genre: Optional[List]
    actors: Optional[List]
    writers: Optional[List]
    directors: Optional[List]

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class Genre(BaseModel):
    uuid: str
    name: str

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class Person(BaseModel):
    uuid: str
    full_name: str
    role: str
    film_ids: Optional[List]

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
