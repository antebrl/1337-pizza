import uuid

import pytest

import app.api.v1.endpoints.dough.crud as dough_crud
from app.api.v1.endpoints.dough.schemas import DoughCreateSchema
from app.database.connection import SessionLocal
from tests.integration.api.v1.helper import clear_db


@pytest.fixture(scope='module')
def db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_dough_create_read_update_delete(db):
    clear_db(db)

    # Instantiate a dough
    dough = DoughCreateSchema(name='test dough', stock=1, price=1, description='test description')

    # Add dough to database
    dough_crud.create_dough(dough, db)

    # Proof correct number of doughs in database
    doughs = dough_crud.get_all_doughs(db)
    assert len(doughs) == 1

    # Proof correct values of doughs in database
    dough = doughs[0]
    assert dough.name == 'test dough'
    assert dough.stock == 1
    assert dough.price == 1
    assert dough.description == 'test description'

    doughs = dough_crud.get_all_doughs(db)
    assert len(doughs) == 1

    # Try to get dough with invalid id
    dough = dough_crud.get_dough_by_id(uuid.UUID('00000000-0000-0000-0000-000000000000'), db)
    assert dough is None

    dou_id = doughs[0].id
    dough = dough_crud.get_dough_by_id(dou_id, db)
    assert dough == doughs[0]

    # Try to get dough with invalid name
    dough = dough_crud.get_dough_by_name('invalid name', db)
    assert dough is None

    dou_name = doughs[0].name
    dough = dough_crud.get_dough_by_name(dou_name, db)
    assert dough == doughs[0]

    changed_dough = DoughCreateSchema(name='test dough1', stock=11, price=11, description='test description1')
    dough_crud.update_dough(doughs[0], changed_dough, db)

    dough = doughs[0]
    assert dough.name == 'test dough1'
    assert dough.stock == 11
    assert dough.price == 11
    assert dough.description == 'test description1'

    # try to delete dough with invalid id
    dough_crud.delete_dough_by_id(uuid.UUID('00000000-0000-0000-0000-000000000000'), db)
    assert len(doughs) == 1

    # Delete dough
    dough_crud.delete_dough_by_id(doughs[0].id, db)
    # Proof correct number of doughs in database after deletion
    doughs = dough_crud.get_all_doughs(db)
    assert len(doughs) == 0

    clear_db(db)