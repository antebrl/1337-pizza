import logging
import uuid

from sqlalchemy.orm import Session

from app.api.v1.endpoints.sauce.schemas import SauceCreateSchema
from app.database.models import Sauce


def create_sauce(schema: SauceCreateSchema, db: Session):
    entity = Sauce(**schema.dict())
    db.add(entity)
    db.commit()
    logging.info('Sauce created with name {}; stock {}; description {}; price {}; spice {}'.format(
        entity.name, entity.stock, entity.description, entity.price, entity.spice))
    return entity


def get_sauce_by_id(sauce_id: uuid.UUID, db: Session):
    entity = db.query(Sauce).filter(Sauce.id == sauce_id).first()
    if not entity:
        logging.error('Sauce with ID {} not found'.format(sauce_id))
    return entity


def get_sauce_by_name(sauce_name: str, db: Session):
    entity = db.query(Sauce).filter(Sauce.name == sauce_name).first()
    if not entity:
        logging.error('Sauce with name {} not found'.format(sauce_name))
    return entity


def get_all_sauces(db: Session):
    return db.query(Sauce).all()


def delete_sauce_by_id(sauce_id: uuid.UUID, db: Session):
    entity = get_sauce_by_id(sauce_id, db)
    if entity:
        db.delete(entity)
        db.commit()
        logging.info('Sauce {} with ID {} deleted'.format(entity.name, sauce_id))
    else:
        logging.error('Sauce with ID {} not found'.format(sauce_id))
