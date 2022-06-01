from http import HTTPStatus
from typing import List, Optional, Union
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel

from core.config import MESSEGE_NON_FOUND
from services.base import Paginator, get_paginator_params
from services.films import (FilmService, FilmsService, get_film_service,
                            get_films_service)

router = APIRouter()


class FilmDitail(BaseModel):
    uuid: UUID
    imdb_rating: Optional[float]
    title: str
    description: str = None
    genre: Optional[List]
    actors: Optional[List]
    writers: Optional[List]
    directors: Optional[List]


class Films(BaseModel):
    uuid: UUID
    title: str
    imdb_rating: Optional[float]


@router.get('/', response_model=List[Films])
async def films_index(
        sort: Union[str, None] = None,
        paginator: Paginator = Depends(get_paginator_params),
        service: FilmsService = Depends(get_films_service)) -> List[Films]:
    data = await service.get_data(sorting=sort, page_size=paginator.page_size, page_number=paginator.page_number)

    if not data:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=MESSEGE_NON_FOUND)

    response = [Films(**dict(row)) for row in data]
    return response


@router.get('/search', response_model=List[Films])
async def films_search(
        query: Union[str, None] = None,
        paginator: Paginator = Depends(get_paginator_params),
        service: FilmsService = Depends(get_films_service)) -> List[Films]:
    data = await service.get_data(search=query, page_size=paginator.page_size, page_number=paginator.page_number)

    if not data:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=MESSEGE_NON_FOUND)

    response = [Films(**dict(row)) for row in data]
    return response


@router.get('/{film_uuid}', response_model=FilmDitail)
async def film_details(film_uuid: UUID, service: FilmService = Depends(get_film_service)) -> FilmDitail:
    film = await service.get_by_uuid(film_uuid)
    response = FilmDitail(**dict(film))
    if not response:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=MESSEGE_NON_FOUND)
    return response
