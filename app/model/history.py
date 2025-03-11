from sqlmodel import Field, SQLModel
import datetime

class History(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    branch_id: int | None = Field(default=None, foreign_key="branch.id")
    created_at: datetime.datetime = Field(
        default_factory=datetime.datetime.utcnow,
    )


class ProductHistory(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    product_id: int | None = Field(default=None, foreign_key="product.id")
    history_id: int | None = Field(default=None, foreign_key="history.id")
    stock_count: int | None = Field(default=None)
    real_count: int | None = Field(default=None)
    image : str | None = Field(default=None)


