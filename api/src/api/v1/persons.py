from http import HTTPStatus
from typing import List, Optional, Union
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic.main import BaseModel

from core.config import MESSEGE_NON_FOUND
from services.base import Paginator, get_paginator_params
from services.persons import (PersonService, PersonsService,
                              get_person_service, get_persons_service)

router = APIRouter()


class Persons(BaseModel):
    uuid: UUID
    full_name: str
    role: str
    film_ids: Optional[List]


@router.get('/', response_model=List[Persons])
async def persons_index(
        paginator: Paginator = Depends(get_paginator_params),
        service: PersonsService = Depends(get_persons_service)) -> List[Persons]:
    data = await service.get_data(page_size=paginator.page_size, page_number=paginator.page_number)
    if not data:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=MESSEGE_NON_FOUND)
    response = [Persons(**dict(row)) for row in data]
    return response


@router.get('/search', response_model=List[Persons])
async def person_search(
        query: Union[str, None] = None,
        paginator: Paginator = Depends(get_paginator_params),
        service: PersonsService = Depends(get_persons_service)) -> List[Persons]:
    data = await service.get_data(search=query, page_size=paginator.page_size, page_number=paginator.page_number)
    if not data:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=MESSEGE_NON_FOUND)
    response = [Persons(**dict(row)) for row in data]
    return response


@router.get('/{person_uuid}', response_model=Persons)
async def person(person_uuid: UUID, service: PersonService = Depends(get_person_service)) -> Persons:
    data = await service.get_by_uuid(person_uuid)
    if not data:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=MESSEGE_NON_FOUND)

    response = Persons(**dict(data))
    return response
