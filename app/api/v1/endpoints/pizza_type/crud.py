import logging
import uuid
from decimal import Decimal

from sqlalchemy.orm import Session

from app.api.v1.endpoints.pizza_type.schemas import (
    PizzaTypeCreateSchema,
    PizzaTypeToppingQuantityCreateSchema,
)
from app.database.models import PizzaType, PizzaTypeToppingQuantity, PizzaTypeSauce


def create_pizza_type(schema: PizzaTypeCreateSchema, db: Session):
    entity = PizzaType(
        name=schema.name,
        price=Decimal(str(schema.price)),
        description=schema.description,
        dough_id=schema.dough_id)

    if not entity:
        logging.warning('PizzaType object is empty')
    logging.info(
        'Trying to create PizzaType ID {}; name {}; description {}'
        .format(entity.id, entity.name, entity.description))
    try:
        db.add(entity)
        db.commit()

        logging.info(
            f'PizzaType ID {entity.id}; name {entity.name}; description {entity.description} stored successfully in '
            f'the database.')

        # Associate sauces with PizzaType
        for sauce_id in schema.sauce_ids:
            pizza_type_sauce = PizzaTypeSauce(pizza_type_id=entity.id, sauce_id=sauce_id)
            db.add(pizza_type_sauce)

        db.commit()
    except Exception as e:
        logging.error(
            f'An error occurred while storing PizzaType ID {entity.id}; name {entity.name}; description '
            f'{entity.description} in the database: Error {e}')
    logging.info(
        'PizzaType created with ID {}; name {}; description {}'
        .format(entity.id, entity.name, entity.description))
    return entity


def get_pizza_type_by_id(pizza_type_id: uuid.UUID, db: Session):
    entity = db.query(PizzaType).filter(PizzaType.id == pizza_type_id).first()
    if not entity:
        logging.error('PizzaType with ID {} not found'.format(pizza_type_id))
    return entity


def get_pizza_type_by_name(pizza_type_name: str, db: Session):
    entity = db.query(PizzaType).filter(PizzaType.name == pizza_type_name).first()
    if not entity:
        logging.error('PizzaType with name {} not found'.format(pizza_type_name))
    return entity


def get_all_pizza_types(db: Session):
    return db.query(PizzaType).all()


def update_pizza_type(pizza_type: PizzaType, changed_pizza_type: PizzaTypeCreateSchema, db: Session):
    for key, value in changed_pizza_type.dict().items():
        setattr(pizza_type, key, value)

    try:
        db.commit()
        db.refresh(pizza_type)
    except Exception as e:
        logging.error(f'PizzaType with ID {pizza_type.id} could not be updated. Error: {e}')
    logging.info('PizzaType with ID {} updated'.format(pizza_type.id))
    return pizza_type


def delete_pizza_type_by_id(pizza_type_id: uuid.UUID, db: Session):
    entity = get_pizza_type_by_id(pizza_type_id, db)
    if entity:
        db.delete(entity)
        db.commit()
        logging.info('PizzaType with ID {} deleted'.format(pizza_type_id))
    else:
        logging.error('Failed to delete PizzaType with ID {}: not found'.format(pizza_type_id))


def create_topping_quantity(
        pizza_type: PizzaType,
        schema: PizzaTypeToppingQuantityCreateSchema,
        db: Session,
):
    entity = PizzaTypeToppingQuantity(**schema.dict())
    logging.info('Trying to create PizzaTypeToppingQuantity created for PizzaType ID {}'.format(pizza_type.id))
    pizza_type.toppings.append(entity)
    db.commit()
    db.refresh(pizza_type)
    logging.info('PizzaTypeToppingQuantity created for PizzaType ID {}'.format(pizza_type.id))
    return entity


def get_topping_quantity_by_id(
        pizza_type_id: uuid.UUID,
        topping_id: uuid.UUID,
        db: Session,
):
    entity = db.query(PizzaTypeToppingQuantity) \
        .filter(PizzaTypeToppingQuantity.topping_id == topping_id,
                PizzaTypeToppingQuantity.pizza_type_id == pizza_type_id) \
        .first()
    if not entity:
        logging.error(
            'Topping quantity with topping ID {} and PizzaType ID {} not found'.format(
                topping_id, pizza_type_id,
            ),
        )
    return entity


def get_joined_topping_quantities_by_pizza_type(
        pizza_type_id: uuid.UUID,
        db: Session,
):
    return db.query(PizzaTypeToppingQuantity) \
        .filter(PizzaTypeToppingQuantity.pizza_type_id == pizza_type_id).all()
