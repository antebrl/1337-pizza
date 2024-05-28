from decimal import Decimal
import uuid
import pytest

import app.api.v1.endpoints.dough.crud as dough_crud
import app.api.v1.endpoints.pizza_type.crud as pizza_type_crud
import app.api.v1.endpoints.order.stock_logic.stock_ingredients_crud as stock_ingredients_crud
import app.api.v1.endpoints.topping.crud as topping_crud
from app.api.v1.endpoints.dough.schemas import DoughCreateSchema
from app.api.v1.endpoints.pizza_type.schemas import PizzaTypeCreateSchema, PizzaTypeToppingQuantityCreateSchema
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


def test_pizza_type_create_read_update_delete(db):
    clear_db(db)
    new_dough_name = 'test'
    new_dough_description = 'test description'
    new_dough_stock = 0
    new_dough_price = Decimal('1.23')
    changed_pizza_type_price = Decimal('1.50')
    number_of_pizza_types_before = len(pizza_type_crud.get_all_pizza_types(db))

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

    new_topping_name = 'test_topping'
    new_topping_description = 'test description'
    new_topping_stock = 5
    new_topping_price = Decimal('1.23')

    # Arrange: Instantiate a new topping object
    topping = ToppingCreateSchema(
        name=new_topping_name,
        stock=new_topping_stock,
        price=new_topping_price,
        description=new_topping_description,
    )

    # Act: Add topping to database
    topping = topping_crud.create_topping(topping, db)
    created_topping_id = topping.id

    new_pizza_type_dough_id = created_dough_id
    new_pizza_type_name = 'Pizza da Fabrizio'
    new_pizza_type_price = Decimal('1.10')
    new_pizza_type_description = 'This is a nice pizza'

    # Arrange: Instantiate a pizza type
    pizza_type = PizzaTypeCreateSchema(
        dough_id=new_pizza_type_dough_id,
        name=new_pizza_type_name,
        price=new_pizza_type_price,
        description=new_pizza_type_description,
    )

    # Act: Add pizza type to database
    pizza_type = pizza_type_crud.create_pizza_type(pizza_type, db)
    created_pizza_type_id = pizza_type.id

    # Assert: One more pizza type in database
    pizza_types = pizza_type_crud.get_all_pizza_types(db)
    assert len(pizza_types) == number_of_pizza_types_before + 1

    # Act: Re-read pizza type from database
    pizza_type = pizza_type_crud.get_pizza_type_by_id(created_pizza_type_id, db)

    # Assert: Proof correct values of pizza type in database
    assert pizza_type.name == new_pizza_type_name
    assert pizza_type.description == new_pizza_type_description
    assert pizza_type.price == new_pizza_type_price
    assert pizza_type.dough_id == new_pizza_type_dough_id

    # Act: Get if ingredients are available for pizza type
    ingredients_available = stock_ingredients_crud.ingredients_are_available(pizza_type)

    # Assert: Try to proof that not enough dough stock is available
    assert ingredients_available is False

    changed_dough_stock = 10
    # Act: Change dough stock
    changed_stock_dough = DoughCreateSchema(
        name=new_dough_name,
        stock=changed_dough_stock,
        price=new_dough_price,
        description=new_dough_description,
    )
    dough_crud.update_dough(dough, changed_stock_dough, db)

    # Assert: Try to get pizza type with invalid id
    invalid_pizza_type = pizza_type_crud.get_pizza_type_by_id(uuid.UUID('00000000-0000-0000-0000-000000000000'), db)
    assert invalid_pizza_type is None

    # Assert: Try to get pizza type with invalid name
    invalid_pizza_type = pizza_type_crud.get_pizza_type_by_name('invalid name', db)
    assert invalid_pizza_type is None

    # Act: Get correct pizza type by name
    pizza_type = pizza_type_crud.get_pizza_type_by_name(new_pizza_type_name, db)

    # Assert: Proof correct values of pizza type in database
    assert pizza_type.name == new_pizza_type_name
    assert pizza_type.description == new_pizza_type_description
    assert pizza_type.price == new_pizza_type_price
    assert pizza_type.dough_id == new_pizza_type_dough_id

    # Act: Change pizza type price
    changed_pizza_type = PizzaTypeCreateSchema(
        dough_id=new_pizza_type_dough_id,
        name=new_pizza_type_name,
        price=changed_pizza_type_price,
        description=new_pizza_type_description,
    )

    pizza_type_crud.update_pizza_type(pizza_type, changed_pizza_type, db)
    pizza_type = pizza_type_crud.get_pizza_type_by_id(created_pizza_type_id, db)

    # Assert: Pizza type price updated
    assert pizza_type.price == changed_pizza_type_price

    new_pizza_type_topping_quantity_quantity = 1

    # Act: Instantiate a PizzaTypeToppingQuantity
    pizza_type_topping_quantity = PizzaTypeToppingQuantityCreateSchema(
        topping_id=created_topping_id,
        quantity=new_pizza_type_topping_quantity_quantity,
    )

    # Act: Add Topping quantity to pizza type
    topping_quantity = pizza_type_crud.create_topping_quantity(pizza_type, pizza_type_topping_quantity, db)

    # Assert: Check created topping_quantity values
    assert topping_quantity.pizza_type == pizza_type
    assert topping_quantity.quantity == new_pizza_type_topping_quantity_quantity
    assert topping_quantity.topping_id == topping.id
    assert topping_quantity.pizza_type_id == pizza_type.id

    # Act: Get topping quantity by id
    topping_quantity = pizza_type_crud.get_topping_quantity_by_id(pizza_type.id, topping.id, db)

    # Assert: Check the returned topping_quantity values
    assert topping_quantity.pizza_type == pizza_type
    assert topping_quantity.quantity == new_pizza_type_topping_quantity_quantity
    assert topping_quantity.topping_id == topping.id
    assert topping_quantity.pizza_type_id == pizza_type.id

    # Act: Get all toppings on pizza type
    toppings = pizza_type_crud.get_joined_topping_quantities_by_pizza_type(pizza_type.id, db)

    # Assert: Amount of toppings is 1
    assert len(toppings) == 1

    # Test Stock Logic

    # Act: Check if ingredients are available
    ingredients_available = stock_ingredients_crud.ingredients_are_available(pizza_type)

    # Assert: ingredients are available
    assert ingredients_available is True

    # Act: increase stock of ingredients by 1
    stock_ingredients_crud.increase_stock_of_ingredients(pizza_type, db)

    # Assert: stock of pizza type dough is now 11
    assert pizza_type.dough.stock == 11

    # Assert: stock of pizza type ingredients is now 6
    assert topping.stock == 6

    # Act: decrease stock of ingredients by 1
    stock_ingredients_crud.reduce_stock_of_ingredients(pizza_type, db)

    # Assert: stock of pizza type dough is now 10
    assert pizza_type.dough.stock == 10

    # Assert: stock of pizza type ingredients is now 5
    assert topping.stock == 5

    # Act: Update Topping stock
    changed_topping_stock = 0

    changed_topping = ToppingCreateSchema(
        name=new_topping_name,
        stock=changed_topping_stock,
        price=new_topping_price,
        description=new_topping_description,
    )
    topping_crud.update_topping(topping, changed_topping, db)

    # Act: Check if ingredients are available
    ingredients_available = stock_ingredients_crud.ingredients_are_available(pizza_type)

    # Assert ingredients are unavailable
    assert ingredients_available is False

    # Assert: try to delete pizza type with invalid id
    pizza_type_crud.delete_pizza_type_by_id(uuid.UUID('00000000-0000-0000-0000-000000000000'), db)
    assert len(pizza_types) == number_of_pizza_types_before + 1

    # Act: Delete dough
    pizza_type_crud.delete_pizza_type_by_id(created_pizza_type_id, db)

    # Assert: Proof correct number of doughs in database after deletion
    pizzas = pizza_type_crud.get_all_pizza_types(db)
    assert len(pizzas) == number_of_pizza_types_before

    # Assert: Correct pizza type was deleted
    pizza = pizza_type_crud.get_pizza_type_by_id(created_pizza_type_id, db)
    assert pizza is None

    # Act: Delete dough
    dough_crud.delete_dough_by_id(created_dough_id, db)

    # Act: Delete topping
    topping_crud.delete_topping_by_id(created_topping_id, db)
