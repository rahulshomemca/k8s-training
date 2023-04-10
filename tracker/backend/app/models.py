from pydantic import BaseModel
from typing import List, Dict

class Todo(BaseModel):
    pass


class Item(BaseModel):
    title: str
    price: float
    hidden: bool


class Category(BaseModel):
    name: str
    items: Dict[str, Item]
    created_at: str