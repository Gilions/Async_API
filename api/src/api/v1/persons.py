from http import HTTPStatus
from typing import List, Optional, Union
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic.main import BaseModel

from core.config import MESSEGE_NON_FOUND
from services.persons import PersonsService, PersonService, get_person_service, get_persons_service

router = APIRouter()


class Persons(BaseModel):
    uuid: UUID
    full_name: str
    role: str
    film_ids: Optional[List]


@router.get('/{person_uuid}', response_model=Persons)
async def persons(person_uuid: UUID, service: PersonService = Depends(get_person_service)) -> Persons:
    data = await service.get_by_uuid(person_uuid)
    if not data:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=MESSEGE_NON_FOUND)

    response = Persons(**dict(data))
    return response


@router.get('/search', response_model=List[Persons])
async def person(
        query: Union[str, None] = None,
        page_size: int = Query(50, alias="page[size]"),
        page_number: int = Query(1, alias="page[number]"),
        service: PersonsService = Depends(get_persons_service)) -> List[Persons]:
    data = await service.get_data(search=query, page_size=page_size, page_number=page_number)
    if not data:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=MESSEGE_NON_FOUND)
    response = [Persons(**dict(row)) for row in data]
    return response
