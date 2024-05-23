from decimal import Decimal
import uuid
import pytest

import app.api.v1.endpoints.dough.crud as dough_crud
from app.api.v1.endpoints.dough.schemas import DoughCreateSchema
from app.database.connection import SessionLocal


@pytest.fixture(scope='module')
def db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_dough_create_read_update_delete(db):
    new_dough_name = 'test'
    new_dough_description = 'test description'
    new_dough_stock = 1
    changed_dough_stock = 3
    new_dough_price = Decimal('1.23')
    number_of_doughs_before = len(dough_crud.get_all_doughs(db))

    # Arrange: Instantiate a dough
    dough = DoughCreateSchema(
        name=new_dough_name,
        stock=new_dough_stock,
        price=new_dough_price,
        description=new_dough_description,
    )

    # Act: Add dough to database
    dough = dough_crud.create_dough(dough, db)
    created_dough_id = dough.id

    # Assert: One more dough in database
    doughs = dough_crud.get_all_doughs(db)
    assert len(doughs) == number_of_doughs_before + 1

    # Act: Re-read dough from database
    dough = dough_crud.get_dough_by_id(created_dough_id, db)

    # Assert: Proof correct values of dough in database
    assert dough.name == new_dough_name
    assert dough.stock == new_dough_stock
    assert dough.price == new_dough_price
    assert dough.description == new_dough_description

    # Assert: Try to get dough with invalid id
    invalid_dough = dough_crud.get_dough_by_id(uuid.UUID('00000000-0000-0000-0000-000000000000'), db)
    assert invalid_dough is None

    # Assert: Try to get dough with invalid name
    invalid_dough = dough_crud.get_dough_by_name('invalid name', db)
    assert invalid_dough is None

    # Act: Get correct dough by name
    dough = dough_crud.get_dough_by_name(new_dough_name, db)

    # Assert: Proof correct values of dough in database
    assert dough.name == new_dough_name
    assert dough.stock == new_dough_stock
    assert dough.price == new_dough_price
    assert dough.description == new_dough_description

    # Act: Change dough stock
    changed_stock_dough = DoughCreateSchema(
        name=new_dough_name,
        stock=changed_dough_stock,
        price=new_dough_price,
        description=new_dough_description,
    )
    dough_crud.update_dough(dough, changed_stock_dough, db)
    dough = dough_crud.get_dough_by_id(created_dough_id, db)

    # Assert: Dough stock updated
    assert dough.stock == changed_dough_stock

    # Assert: try to delete dough with invalid id
    dough_crud.delete_dough_by_id(uuid.UUID('00000000-0000-0000-0000-000000000000'), db)
    assert len(doughs) == number_of_doughs_before + 1

    # Act: Delete dough
    dough_crud.delete_dough_by_id(created_dough_id, db)

    # Assert: Proof correct number of doughs in database after deletion
    doughs = dough_crud.get_all_doughs(db)
    assert len(doughs) == number_of_doughs_before

    # Assert: Correct user was deleted
    dough = dough_crud.get_dough_by_id(created_dough_id, db)
    assert dough is None
