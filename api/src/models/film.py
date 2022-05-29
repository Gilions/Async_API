from typing import Optional, List

import orjson

from pydantic import BaseModel, Field


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


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
