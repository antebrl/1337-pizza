import uuid
from typing import List

from fastapi import APIRouter, Depends, Request, status, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from starlette.responses import Response

import app.api.v1.endpoints.sauce.crud as sauce_crud
from app.api.v1.endpoints.sauce.schemas import SauceSchema, SauceCreateSchema, SauceListItemSchema
from app.database.connection import SessionLocal

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get('', response_model=List[SauceListItemSchema], tags=['sauce'])
def get_all_sauces(db: Session = Depends(get_db)):
    return sauce_crud.get_all_sauces(db)


@router.get('/{sauce_id}', response_model=SauceSchema, tags=['sauce'])
def get_sauce(sauce_id: uuid.UUID,
              db: Session = Depends(get_db),
              ):
    sauce = sauce_crud.get_sauce_by_id(sauce_id, db)

    if not sauce:
        raise HTTPException(status_code=404, detail='Sauce with ID {} not found'.format(sauce_id))
    return sauce


@router.post('', response_model=SauceSchema, status_code=status.HTTP_201_CREATED, tags=['sauce'])
def create_sauce(sauce: SauceCreateSchema,
                 request: Request,
                 db: Session = Depends(get_db),
                 ):
    sauce_found = sauce_crud.get_sauce_by_name(sauce.name, db)
    if sauce_found:
        url = request.url_for('get_sauce', sauce_id=sauce_found.id)
        return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)

    new_sauce = sauce_crud.create_sauce(sauce, db)
    return new_sauce


@router.delete('/{sauce_id}', response_model=None, tags=['sauce'])
def delete_sauce(sauce_id: uuid.UUID, db: Session = Depends(get_db)):
    sauce = sauce_crud.get_sauce_by_id(sauce_id, db)

    if not sauce:
        raise HTTPException(status_code=404, detail='Sauce with ID {} not deleted (not found)'.format(sauce_id))

    sauce_crud.delete_sauce_by_id(sauce_id, db)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
