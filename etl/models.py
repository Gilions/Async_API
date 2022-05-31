from typing import List, Optional

from pydantic import BaseModel, Field


class Movies(BaseModel):
    uuid: str
    imdb_rating: Optional[float] = Field(default=0)
    title: str
    description: str = None
    genre: Optional[List]
    directors: Optional[List]
    writers: Optional[List]
    actors: Optional[List]


class Genres(BaseModel):
    uuid: str
    name: str


class Persons(BaseModel):
    uuid: str
    full_name: str
    role: str
    film_ids: Optional[List]
