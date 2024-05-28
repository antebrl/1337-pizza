import pytest

from app.api.v1.endpoints.order.address.schemas import AddressCreateSchema
from app.database.connection import SessionLocal
import app.api.v1.endpoints.order.address.crud as address_crud


@pytest.fixture(scope='module')
def db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def fetch_and_compare_address(address, db):
    resolved_address = address_crud.get_address_by_id(address.id, db)
    assert resolved_address.street == address.street
    assert resolved_address.house_number == address.house_number
    assert resolved_address.country == address.country
    assert resolved_address.town == address.town
    assert resolved_address.first_name == address.first_name
    assert resolved_address.last_name == address.last_name
    assert resolved_address.post_code == address.post_code


def test_address_create_read_update_delete(db):
    number_of_addresses_before = len(address_crud.get_all_addresses(db))

    # Arrange: Instantiate address
    address_schema = AddressCreateSchema(
        street='Testweg', post_code='64283', house_number=1,
        country='Germany', town='Darmstadt', first_name='Test', last_name='User')

    # Act: Add address to database
    address = address_crud.create_address(address_schema, db)

    # Assert: Proof correct number of addresses in database
    addresses = address_crud.get_all_addresses(db)
    assert len(addresses) == number_of_addresses_before + 1

    # Assert: Proof that we get correct address using id
    fetch_and_compare_address(address, db)

    # Arrange: Instantiate changed address
    changed_address = AddressCreateSchema(
        street='Teststr', post_code='68161', house_number=1,
        country='Germany', town='Mannheim', first_name='Test', last_name='User')

    # Act: Update address to changed address
    updated_address = address_crud.update_address(address, changed_address, db)

    # Assert: Proof that we get correct address using id
    fetch_and_compare_address(updated_address, db)

    # Act: delete address in db
    address_crud.delete_address_by_id(address.id, db)

    resolved_address = address_crud.get_address_by_id(address.id, db)
    # Assert: Proof that the address was deleted
    assert resolved_address is None
