from sqlmodel import Field, SQLModel, Relationship
from app.model.branch_category import BranchCategory
from app.model.product import Product



class BranchCategoryProduct(SQLModel, table=True):
    branch_category_branch_id: int = Field(
        foreign_key="branchcategory.branch_id", primary_key=True
    )
    branch_category_category_id: int = Field(
        foreign_key="branchcategory.category_id", primary_key=True
    )
    branch_category: BranchCategory = Relationship(back_populates="products")
    
    product_id: int | None = Field(default=None, foreign_key="product.id", primary_key=True)
    product : Product = Relationship(back_populates="categories")

    priority: int = Field(default=None)
    quantity: int = Field(default=None)