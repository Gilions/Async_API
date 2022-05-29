from http import HTTPStatus
from typing import Optional, List, Union

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel

from services.films import FilmsService, FilmService, get_film_service, get_films_service


router = APIRouter()


class FilmDitail(BaseModel):
    uuid: str
    imdb_rating: Optional[float]
    title: str
    description: str = None
    genre: Optional[List]
    actors: Optional[List]
    writers: Optional[List]
    directors: Optional[List]


class Films(BaseModel):
    uuid: str
    title: str
    imdb_rating: Optional[float]


@router.get('', response_model=List[Films])
async def films(
        sort: Union[str, None] = None,
        page_size: int = Query(50, alias="page[size]"),
        page_number: int = Query(1, alias="page[number]"),
        films_service: FilmsService = Depends(get_films_service)) -> List[Films]:
    response = [
        Films(**dict(film))
        for film in await films_service.get_films(sorting=sort, page_size=page_size, page_number=page_number)]
    if not response:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='film not found')
    return response


@router.get('/search', response_model=List[Films])
async def films_search(
        query: Union[str, None] = None,
        page_size: int = Query(50, alias="page[size]"),
        page_number: int = Query(1, alias="page[number]"),
        films_service: FilmsService = Depends(get_films_service)) -> List[Films]:
    response = [
        Films(**dict(data))
        for data in await films_service.get_films(search=query, page_size=page_size, page_number=page_number)]
    if not response:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='film not found')
    return response


@router.get('/{film_id}', response_model=FilmDitail)
async def film_details(film_id: str, film_service: FilmService = Depends(get_film_service)) -> FilmDitail:
    film = await film_service.get_by_id(film_id)
    response = FilmDitail(**dict(film))
    if not response:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='film not found')
    return response

