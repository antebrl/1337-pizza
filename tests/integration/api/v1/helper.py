import app.api.v1.endpoints.order.crud as order_crud
import app.api.v1.endpoints.order.address.crud as address_crud
import app.api.v1.endpoints.user.crud as user_crud
import app.api.v1.endpoints.dough.crud as dough_crud
import app.api.v1.endpoints.pizza_type.crud as pizza_type_crud
import app.api.v1.endpoints.beverage.crud as beverage_crud
import app.api.v1.endpoints.topping.crud as topping_crud


def clear_db(db):

    # Delete all users in db
    users = user_crud.get_all_users(db)
    for user in users:
        user_crud.delete_user_by_id(user.id, db)

    # Delete addresses in db
    addresses = address_crud.get_all_addresses(db)
    for address in addresses:
        address_crud.delete_address_by_id(address.id, db)

    # create variables for deleting stuff
    doughs = dough_crud.get_all_doughs(db)
    pizza_types = pizza_type_crud.get_all_pizza_types(db)
    orders = order_crud.get_all_orders(db)
    toppings = topping_crud.get_all_toppings(db)
    # delete all pizzas due to foreign constraint
    for order in orders:
        pizzas = order_crud.get_all_pizzas_of_order(order, db)
        for piz in pizzas:
            order_crud.delete_pizza_from_order(order, piz.id, db)
    # delete all pizza_types due to foreign constraint
    for piz in pizza_types:
        pizza_type_crud.delete_pizza_type_by_id(piz.id, db)
    # delete all toppings
    for topping in toppings:
        topping_crud.delete_topping_by_id(topping.id, db)
    # delete doughs
    for dou in doughs:
        dough_crud.delete_dough_by_id(dou.id, db)

    # delete all beverages
    beverages = beverage_crud.get_all_beverages(db)
    for bev in beverages:
        beverage_crud.delete_beverage_by_id(bev.id, db)
