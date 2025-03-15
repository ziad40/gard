from sqlmodel import Field, SQLModel, Relationship
from typing import List, TYPE_CHECKING
from app.model.branch import Branch
from app.model.category import Category
if TYPE_CHECKING:
    from app.model.branch_category_product import BranchCategoryProduct


class BranchCategory(SQLModel, table=True):
    category_id: int | None = Field(default=None, foreign_key="category.id", primary_key=True)
    branch_id: int | None = Field(default=None, foreign_key="branch.id", primary_key=True)
    priority: int = Field(default=None)

    branch: Branch = Relationship(back_populates="categories")
    category: Category = Relationship(back_populates="branches")

    products: List["BranchCategoryProduct"] = Relationship(back_populates="branch_category")