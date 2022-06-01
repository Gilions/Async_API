from http import HTTPStatus
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic.main import BaseModel

from core.config import MESSEGE_NON_FOUND
from services.base import Paginator, get_paginator_params
from services.genres import (GenreService, GenresService, get_genre_service,
                             get_genres_service)

router = APIRouter()


class Genres(BaseModel):
    uuid: UUID
    name: str


@router.get('/', response_model=List[Genres])
async def genres_index(
        paginator: Paginator = Depends(get_paginator_params),
        service: GenresService = Depends(get_genres_service)) -> List[Genres]:
    data = await service.get_data(page_size=paginator.page_size, page_number=paginator.page_number)

    if not data:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=MESSEGE_NON_FOUND)

    response = [Genres(**dict(row)) for row in data]
    return response


@router.get('/{genre_uuid}', response_model=Genres)
async def genre(genre_uuid: UUID, service: GenreService = Depends(get_genre_service)) -> Genres:
    data = await service.get_by_uuid(genre_uuid)
    response = Genres(**dict(data))
    if not response:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=MESSEGE_NON_FOUND)
    return response
