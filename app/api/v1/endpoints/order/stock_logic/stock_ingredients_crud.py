import logging

from sqlalchemy.orm import Session

from app.database.models import PizzaType


def ingredients_are_available(pizza_type: PizzaType):
    if pizza_type.dough.stock <= 0:
        logging.error(
            'PizzaType {} with id {} has not enough dough with ID {} in stock. Dough name: {}, Dough stock: {}'.format(
                pizza_type.name, pizza_type.id, pizza_type.dough_id, pizza_type.dough.name, pizza_type.dough.stock))
        return False

    for topping_quantity in pizza_type.toppings:
        if topping_quantity.topping.stock < topping_quantity.quantity:
            logging.error(
                'PizzaType {} with id {} has not enough topping with ID {} in stock. Topping name: {}, '
                'Topping Stock: {}, Topping needed: {}'.format(
                    pizza_type.name,
                    pizza_type.id,
                    topping_quantity.topping.name,
                    topping_quantity.topping.id,
                    topping_quantity.topping.stock,
                    topping_quantity.quantity))

            return False

    return True


def reduce_stock_of_ingredients(pizza_type: PizzaType, db: Session):
    pizza_type.dough.stock -= 1

    toppings_info = []
    for topping_quantity in pizza_type.toppings:
        topping_quantity.topping.stock -= topping_quantity.quantity
        toppings_info.append({
            'topping_id': topping_quantity.topping.id,
            'quantity': topping_quantity.quantity,
            'new_stock': topping_quantity.topping.stock,
        })

    db.commit()
    logging.info(f'Reduced stock of ingredients for pizza type {pizza_type.id}. Toppings: {toppings_info}')


def increase_stock_of_ingredients(pizza_type: PizzaType, db: Session):
    pizza_type.dough.stock += 1

    toppings_info = []
    for topping_quantity in pizza_type.toppings:
        topping_quantity.topping.stock += topping_quantity.quantity
        toppings_info.append({
            'topping_id': topping_quantity.topping.id,
            'quantity': topping_quantity.quantity,
            'new_stock': topping_quantity.topping.stock,
        })

    db.commit()
    logging.info(f'Increased stock of ingredients for pizza type {pizza_type.id}. Toppings: {toppings_info}')
