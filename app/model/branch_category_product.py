from sqlmodel import Field, SQLModel, Relationship, UniqueConstraint
from app.model.product import Product
from typing import TYPE_CHECKING, Optional
if TYPE_CHECKING:
    from app.model.branch_category import BranchCategory



class BranchCategoryProduct(SQLModel, table=True):
    branch_category_branch_id: int = Field(
        foreign_key="branch.id", primary_key=True
    )
    branch_category_category_id: int = Field(
        foreign_key="category.id", primary_key=True
    )
    product_id: int | None = Field(default=None, foreign_key="product.id", primary_key=True)
    
    product : Product = Relationship(back_populates="categories")

    priority: Optional[int] = Field(default=None)
    quantity: int = Field(default=None)

    __table_args__ = (UniqueConstraint("branch_category_category_id", "priority", name="uq_category_priority"),)
