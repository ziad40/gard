from sqlmodel import Field, SQLModel, Relationship
from typing import TYPE_CHECKING, List
if TYPE_CHECKING:
    from app.model.branch_category_product import BranchCategoryProduct

class Product(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    
    categories: List["BranchCategoryProduct"] = Relationship(
        back_populates="product"
    )