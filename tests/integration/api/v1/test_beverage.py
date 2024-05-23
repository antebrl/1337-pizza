import pytest

import app.api.v1.endpoints.beverage.crud as beverage_crud
from app.api.v1.endpoints.beverage.schemas import BeverageCreateSchema
from app.database.connection import SessionLocal
from tests.integration.api.v1.helper import clear_db


@pytest.fixture(scope='module')
def db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_beverage_create_read_delete(db):
    clear_db(db)
    new_beverage_name = 'test_beverage'
    number_of_beverages_before = len(beverage_crud.get_all_beverages(db))

    # Arrange: Instantiate a new beverage object
    beverage = BeverageCreateSchema(name=new_beverage_name, stock=1, price=1, description='test description')

    # Act: Add beverage to database
    db_beverage = beverage_crud.create_beverage(beverage, db)
    created_beverage_id = db_beverage.id

    # Assert: One more beverage in database
    beverages = beverage_crud.get_all_beverages(db)
    assert len(beverages) == number_of_beverages_before + 1

    # Act: Re-read beverage from database
    read_beverage = beverage_crud.get_beverage_by_id(created_beverage_id, db)

    # Assert: Correct beverage was stored in database
    assert read_beverage.id == created_beverage_id
    assert read_beverage.name == new_beverage_name
    assert read_beverage.stock == 1
    assert read_beverage.price == 1
    assert read_beverage.description == 'test description'

    # Act: Delete beverage
    beverage_crud.delete_beverage_by_id(created_beverage_id, db)

    # Assert: Correct number of beverages in database after deletion
    beverages = beverage_crud.get_all_beverages(db)
    assert len(beverages) == number_of_beverages_before

    # Assert: Correct beverage was deleted from database
    deleted_beverage = beverage_crud.get_beverage_by_id(created_beverage_id, db)
    assert deleted_beverage is None
