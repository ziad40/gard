from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from app.model.category import Category

class Product(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    category_id: int | None = Field(default=None, foreign_key="category.id")
    category: Optional["Category"] = Relationship(back_populates="products")