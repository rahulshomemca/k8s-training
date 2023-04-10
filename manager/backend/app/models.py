from pydantic import BaseModel
from typing import Optional

class Todo(BaseModel):
    title: str
    price: float
    category: str
    hidden: bool = False
    created_at:  Optional[str] = None