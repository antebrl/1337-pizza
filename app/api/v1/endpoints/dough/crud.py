import logging
import uuid

from sqlalchemy.orm import Session

from app.api.v1.endpoints.dough.schemas import DoughCreateSchema
from app.database.models import Dough


def create_dough(schema: DoughCreateSchema, db: Session):
    entity = Dough(**schema.dict())
    db.add(entity)
    db.commit()
    logging.info('Dough created with name {}; price {}; stock {}; description {}'.format(
        entity.name, entity.price, entity.stock, entity.description))
    return entity


def get_dough_by_id(dough_id: uuid.UUID, db: Session):
    entity = db.query(Dough).filter(Dough.id == dough_id).first()
    if not entity:
        logging.error('Dough with ID {} not found'.format(dough_id))
    else:
        logging.info('Dough retrieved with ID {}'.format(dough_id))
    return entity


def get_dough_by_name(dough_name: str, db: Session):
    entity = db.query(Dough).filter(Dough.name == dough_name).first()
    if entity:
        logging.info('Dough retrieved with name {}'.format(dough_name))
    else:
        logging.error('Dough with name {} not found'.format(dough_name))
    return entity


def get_all_doughs(db: Session):
    logging.info('Retrieving all doughs')
    return db.query(Dough).all()


def update_dough(dough: Dough, changed_dough: DoughCreateSchema, db: Session):
    original_values = {key: getattr(dough, key) for key in changed_dough.dict()}
    for key, value in changed_dough.dict().items():
        setattr(dough, key, value)
    db.commit()
    db.refresh(dough)
    logging.info('Dough updated from {} to {}'.format(original_values, changed_dough.dict()))
    return dough


def delete_dough_by_id(dough_id: uuid.UUID, db: Session):
    entity = get_dough_by_id(dough_id, db)
    if entity:
        db.delete(entity)
        db.commit()
        logging.info('Dough with ID {} deleted'.format(dough_id))
    else:
        logging.error('Failed to delete dough with ID {}: not found'.format(dough_id))
