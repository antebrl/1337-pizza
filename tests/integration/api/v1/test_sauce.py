from decimal import Decimal
import uuid
import pytest

import app.api.v1.endpoints.sauce.crud as sauce_crud
from app.api.v1.endpoints.sauce.schemas import SauceCreateSchema, SpiceLevel
from app.database.connection import SessionLocal


@pytest.fixture(scope='module')
def db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_sauce_create_read_delete(db):
    new_sauce_name = 'test'
    new_sauce_description = 'test description'
    new_sauce_stock = 1
    new_sauce_price = Decimal('1.23')
    new_sauce_spice = SpiceLevel.MEDIUM
    number_of_sauces_before = len(sauce_crud.get_all_sauces(db))

    # Arrange: Instantiate a sauce
    sauce = SauceCreateSchema(
        name=new_sauce_name,
        stock=new_sauce_stock,
        price=new_sauce_price,
        spice=new_sauce_spice,
        description=new_sauce_description,
    )

    # Act: Add sauce to database
    sauce = sauce_crud.create_sauce(sauce, db)
    created_sauce_id = sauce.id

    # Assert: One more sauce in database
    sauces = sauce_crud.get_all_sauces(db)
    assert len(sauces) == number_of_sauces_before + 1

    # Act: Re-read sauce from database
    sauce = sauce_crud.get_sauce_by_id(created_sauce_id, db)

    # Assert: Proof correct values of sauce in database
    assert sauce.name == new_sauce_name
    assert sauce.stock == new_sauce_stock
    assert sauce.price == new_sauce_price
    assert sauce.description == new_sauce_description
    assert sauce.spice == new_sauce_spice

    # Assert: Try to get sauce with invalid id
    invalid_sauce = sauce_crud.get_sauce_by_id(uuid.UUID('00000000-0000-0000-0000-000000000000'), db)
    assert invalid_sauce is None

    # Assert: Try to get sauce with invalid name
    invalid_sauce = sauce_crud.get_sauce_by_name('invalid name', db)
    assert invalid_sauce is None

    # Act: Get correct sauce by name
    sauce = sauce_crud.get_sauce_by_name(new_sauce_name, db)

    # Assert: Proof correct values of sauce in database
    assert sauce.name == new_sauce_name
    assert sauce.stock == new_sauce_stock
    assert sauce.price == new_sauce_price
    assert sauce.description == new_sauce_description

    # Assert: try to delete sauce with invalid id
    sauce_crud.delete_sauce_by_id(uuid.UUID('00000000-0000-0000-0000-000000000000'), db)
    assert len(sauces) == number_of_sauces_before + 1

    # Act: Delete sauce
    sauce_crud.delete_sauce_by_id(created_sauce_id, db)

    # Assert: Proof correct number of sauces in database after deletion
    sauces = sauce_crud.get_all_sauces(db)
    assert len(sauces) == number_of_sauces_before

    # Assert: Correct sauce was deleted
    sauce = sauce_crud.get_sauce_by_id(created_sauce_id, db)
    assert sauce is None
