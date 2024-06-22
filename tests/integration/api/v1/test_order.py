import uuid
import pytest

import app.api.v1.endpoints.dough.crud as dough_crud
from app.api.v1.endpoints.beverage.schemas import BeverageCreateSchema
from app.api.v1.endpoints.dough.schemas import DoughCreateSchema
from app.api.v1.endpoints.order.address.schemas import AddressCreateSchema
from app.api.v1.endpoints.order.schemas import OrderCreateSchema, OrderStatus
from app.api.v1.endpoints.pizza_type.schemas import PizzaTypeCreateSchema
from app.api.v1.endpoints.topping.schemas import ToppingCreateSchema
from app.api.v1.endpoints.user.schemas import UserCreateSchema
from app.database.connection import SessionLocal
import app.api.v1.endpoints.user.crud as user_crud
import app.api.v1.endpoints.beverage.crud as beverage_crud
import app.api.v1.endpoints.topping.crud as topping_crud
import app.api.v1.endpoints.order.address.crud as address_crud
import app.api.v1.endpoints.pizza_type.crud as pizza_type_crud
import app.api.v1.endpoints.order.crud as order_crud
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
    number_of_orders_before = len(order_crud.get_all_orders(db))
    number_of_orders_preparing_before = len(order_crud.get_all_orders(db, OrderStatus.PREPARING))
    test_description = 'test description'

    # Arrange: Instantiate all components

    # Instantiate user
    user_schema = UserCreateSchema(username='test user')
    user = user_crud.create_user(user_schema, db)

    # Instantiate dough
    dough_schema = DoughCreateSchema(name='test dough', price=1, description='test dough description', stock=2)
    dough = dough_crud.create_dough(dough_schema, db)

    # Instantiate a topping
    topping_schema = ToppingCreateSchema(name='test topping', price=1, stock=2, description=test_description)
    topping = topping_crud.create_topping(topping_schema, db)

    # Instantiate a Pizza_type
    pizza_type_schema = PizzaTypeCreateSchema(
        name='update_pizza_type',
        price=5,
        description='update_pizza_type description',
        dough_id=dough.id)
    pizza_type = pizza_type_crud.create_pizza_type(pizza_type_schema, db)

    # Instantiate a beverage
    beverage_schema = BeverageCreateSchema(name='test beverage', stock=2, price=1, description=test_description)
    # Add beverage to database
    beverage = beverage_crud.create_beverage(beverage_schema, db)

    # Add second beverage
    second_beverage_schema = BeverageCreateSchema(
        name='test beverage 2',
        stock=2,
        price=2,
        description=test_description,
    )
    second_beverage = beverage_crud.create_beverage(second_beverage_schema, db)

    # Instantiate address
    address_schema = AddressCreateSchema(
        street='Testweg', post_code='64283', house_number=1,
        country='Germany', town='Darmstadt', first_name='Test', last_name='User')
    # Add address to database
    address = address_crud.create_address(address_schema, db)

    # Instantiate order
    order_schema = OrderCreateSchema(address=address, user_id=user.id)
    order = order_crud.create_order(order_schema, db)

    # Act: Update the order status
    updated_order = order_crud.update_order_status(order, OrderStatus.PREPARING, db)

    # Assert: Check if the status has been updated correctly
    assert updated_order.order_status == OrderStatus.PREPARING

    # Retrieve the order and check the status
    resolved_order = order_crud.get_order_by_id(order.id, db)
    assert resolved_order.order_status == OrderStatus.PREPARING

    orders = order_crud.get_all_orders(db, OrderStatus.PREPARING)
    assert len(orders) == number_of_orders_preparing_before + 1

    orders = order_crud.get_all_orders(db)
    assert len(orders) == number_of_orders_before + 1

    # try invalid order id
    false_order = order_crud.get_order_by_id(uuid.UUID('00000000-0000-0000-0000-000000000000'), db)
    assert false_order is None

    # Proof that we get correct order using id
    resolved_order = order_crud.get_order_by_id(order.id, db)
    assert order.order_status == resolved_order.order_status
    assert order.order_datetime == resolved_order.order_datetime
    assert order.id == resolved_order.id
    assert order.user_id == resolved_order.user_id
    assert order.address_id == resolved_order.address_id
    assert order.beverages == resolved_order.beverages
    assert order.pizzas == resolved_order.pizzas

    pizzas_in_order_before = len(order_crud.get_all_pizzas_of_order(order, db))
    pizza = order_crud.add_pizza_to_order(order, pizza_type, db)
    pizzas_in_order = order_crud.get_all_pizzas_of_order(order, db)
    assert len(pizzas_in_order) == pizzas_in_order_before + 1

    order_price = order_crud.get_price_of_order(order.id, db)
    assert order_price == 5

    order_crud.delete_pizza_from_order(order, pizza.id, db)
    pizzas_in_order = order_crud.get_all_pizzas_of_order(order, db)
    assert len(pizzas_in_order) == pizzas_in_order_before

    order_crud.delete_order_by_id(order.id, db)

    # Assert: Proof correct number of orders in database after deletion
    orders = order_crud.get_all_orders(db)
    assert len(orders) == number_of_orders_before

    # Assert: Correct order was deleted
    deleted_order = order_crud.get_order_by_id(order.id, db)
    assert deleted_order is None

    address_crud.delete_address_by_id(address.id, db)
    beverage_crud.delete_beverage_by_id(beverage.id, db)
    beverage_crud.delete_beverage_by_id(second_beverage.id, db)
    pizza_type_crud.delete_pizza_type_by_id(pizza_type.id, db)
    topping_crud.delete_topping_by_id(topping.id, db)
    dough_crud.delete_dough_by_id(dough.id, db)
    user_crud.delete_user_by_id(user.id, db)
