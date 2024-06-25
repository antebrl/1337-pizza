import uuid
from enum import Enum

from pydantic import BaseModel


class SpiceLevel(str, Enum):
    MILD = 'MILD'
    MEDIUM = 'MEDIUM'
    HOT = 'HOT'


class SauceBaseSchema(BaseModel):
    name: str
    description: str
    price: float
    spice: SpiceLevel

    class Config:
        orm_mode = True


class SauceCreateSchema(SauceBaseSchema):
    stock: int


class SauceSchema(SauceCreateSchema):
    id: uuid.UUID


class SauceListItemSchema(BaseModel):
    id: uuid.UUID
    name: str
    description: str
    price: float
    spice: SpiceLevel

    class Config:
        orm_mode = True
