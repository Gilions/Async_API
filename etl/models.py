from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, validator


class Actors(BaseModel):
    id: str = Field(alias='person_id')
    name: str = Field(alias='person_name')


class Writers(BaseModel):
    id: str = Field(alias='person_id')
    name: str = Field(alias='person_name')


class Movies(BaseModel):
    id: str
    imdb_rating: Optional[float] = Field(alias='rating', default=0)
    title: str
    description: str = None
    genre: Optional[List] = Field(alias='genres')
    director: Optional[List] = Field(alias='director')
    writers: List[Writers] = Field(alias='writers')
    writers_names: Optional[List] = Field(alias='writers_names')
    actors: List[Actors] = Field(alias='actors')
    actors_names: Optional[List] = Field(alias='actors_names')

    @validator('director')
    def validate_director(cls, v):
        return v or []


class Genres(BaseModel):
    id: str
    name: str
    description: str = None


class Persons(BaseModel):
    id: str
    full_name: str
    birth_date: datetime = None
