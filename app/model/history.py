from sqlmodel import Field, SQLModel, Relationship
import datetime
from typing import Optional, List, TYPE_CHECKING
from app.model.branch import Branch
from app.model.product import Product
from app.model.category import Category


class History(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    branch_id: int | None = Field(default=None, foreign_key="branch.id")
    category_id: int | None = Field(default=None, foreign_key="category.id")
    next_product_order: int | None = Field(default=None)
    prev_product_id: int | None = Field(default=None)
    created_at: datetime.datetime = Field(
        default_factory=datetime.datetime.utcnow,
    )
    branch: Optional[Branch] = Relationship(sa_relationship_kwargs={"lazy": "joined"})
    category: Optional[Category] = Relationship(sa_relationship_kwargs={"lazy": "joined"})
    products : List["ProductHistory"] = Relationship(back_populates="history")


class ProductHistory(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    product_id: int | None = Field(default=None, foreign_key="product.id")
    history_id: int | None = Field(default=None, foreign_key="history.id")
    stock_count: int | None = Field(default=None)
    real_count: int | None = Field(default=None)
    state: str | None = Field(default=None)
    image : str | None = Field(default=None)

    product: Optional[Product] = Relationship(sa_relationship_kwargs={"lazy": "joined"})
    history: Optional["History"] = Relationship(back_populates="products")
