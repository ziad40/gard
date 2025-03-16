from sqlmodel import Field, SQLModel, Relationship
from typing import List, Optional
from app.model.branch import Branch
from app.model.category import Category
from app.model.branch_category_product import BranchCategoryProduct


class BranchCategory(SQLModel, table=True):
    category_id: int | None = Field(default=None, foreign_key="category.id", primary_key=True)
    branch_id: int | None = Field(default=None, foreign_key="branch.id", primary_key=True)
    priority: Optional[int] = Field(default=None)

    branch: Branch = Relationship(back_populates="categories")
    category: Category = Relationship(back_populates="branches")
