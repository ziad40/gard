from sqlmodel import Field, SQLModel


class BranchCategoryProductLink(SQLModel, table=True):
    branch_id: int | None = Field(default=None, foreign_key="branch.id", primary_key=True)
    category_id: int | None = Field(default=None, foreign_key="category.id", primary_key=True)
    product_id: int | None = Field(default=None, foreign_key="product.id", primary_key=True)
    priority: int = Field(default=None)
    quantity: int = Field(default=None)