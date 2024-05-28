import pytest

import app.api.v1.endpoints.topping.crud as topping_crud
from app.api.v1.endpoints.topping.schemas import ToppingCreateSchema
from app.database.connection import SessionLocal
from tests.integration.api.v1.helper import clear_db


@pytest.fixture(scope='module')
def db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_topping_create_read_delete(db):
    clear_db(db)
    new_topping_name = 'test_topping'
    new_topping_description = 'test description'
    number_of_toppings_before = len(topping_crud.get_all_toppings(db))

    # Arrange: Instantiate a new topping object
    topping = ToppingCreateSchema(
        name=new_topping_name,
        stock=1,
        price=1,
        description=new_topping_description,
    )

    # Act: Add topping to database
    db_topping = topping_crud.create_topping(topping, db)
    created_topping_id = db_topping.id

    # Assert: One more topping in database
    toppings = topping_crud.get_all_toppings(db)
    assert len(toppings) == number_of_toppings_before + 1

    # Act: Re-read topping from database
    read_topping = topping_crud.get_topping_by_id(created_topping_id, db)

    # Assert: Correct topping was stored in database
    assert read_topping.id == created_topping_id
    assert read_topping.name == new_topping_name
    assert read_topping.stock == 1
    assert read_topping.price == 1
    assert read_topping.description == 'test description'

    read_topping = topping_crud.get_topping_by_name(new_topping_name, db)
    assert read_topping.id == created_topping_id

    # Act: Update topping
    updated_topping_name = 'updated_test_topping'
    updated_topping_description = 'updated test description'
    updated_topping = ToppingCreateSchema(
        name=updated_topping_name,
        stock=2,
        price=2,
        description=updated_topping_description,
    )
    updated_db_topping = topping_crud.update_topping(read_topping, updated_topping, db)

    # Assert: Topping was updated correctly in the database
    assert updated_db_topping.id == created_topping_id
    assert updated_db_topping.name == updated_topping_name
    assert updated_db_topping.stock == 2
    assert updated_db_topping.price == 2
    assert updated_db_topping.description == updated_topping_description

    # Act: Delete topping
    topping_crud.delete_topping_by_id(created_topping_id, db)

    # Assert: Correct number of toppings in database after deletion
    toppings = topping_crud.get_all_toppings(db)
    assert len(toppings) == number_of_toppings_before

    # Assert: Correct topping was deleted from database
    deleted_topping = topping_crud.get_topping_by_id(created_topping_id, db)
    assert deleted_topping is None
