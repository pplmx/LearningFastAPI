from enum import Enum
from typing import Optional

from pydantic import BaseModel


class ModelName(str, Enum):
    AlexNet = "AlexNet"
    ResNet = "ResNet"
    LeNet = "LeNet"


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
