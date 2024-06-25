import logging

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


def get_sauce_by_name(sauce_name: str, db: Session):
    entity = db.query(Sauce).filter(Sauce.name == sauce_name).first()
    if not entity:
        logging.error('Sauce with name {} not found'.format(sauce_name))
    return entity


def get_all_sauces(db: Session):
    return db.query(Sauce).all()
