import uuid
import logging

from sqlalchemy.orm import Session

import app.api.v1.endpoints.beverage.crud as beverage_crud
from app.database.models import Beverage


def beverage_is_available(beverage_id: uuid.UUID, amount: int, db: Session):
    # Get Beverage
    beverage = beverage_crud.get_beverage_by_id(beverage_id, db)
    # Check if Beverage exists
    if beverage:
        # If there is enough stock return true. Stock CAN be zero
        return beverage.stock >= amount
    else:
        logging.error(f'Beverage with ID {beverage_id} does not exist.')
        return False


def change_stock_of_beverage(beverage_id: uuid.UUID, change_amount: int, db: Session):
    # Get Beverage
    beverage = db.query(Beverage).filter(Beverage.id == beverage_id).first()

    # Check if Beverage exists and if Stock is not getting smaller than zero
    if beverage:
        if beverage.stock + change_amount >= 0:
            setattr(beverage, 'stock', beverage.stock + change_amount)
            db.commit()
            db.refresh(beverage)
            return True
        else:
            logging.error(
                f'Stock change would result in negative stock for beverage {beverage_id}. '
                f'Current stock: {beverage.stock}, Change amount: {change_amount}',
            )
            return False

    logging.error(f'Beverage with ID {beverage_id} does not exist.')
    return False
