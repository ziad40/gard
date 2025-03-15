from sqlmodel import Field, SQLModel, Relationship
from typing import TYPE_CHECKING, List
if TYPE_CHECKING:
    from app.model.branch_category import BranchCategory
    
class Category(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    
    branches: List["BranchCategory"] = Relationship(
        back_populates="category"
    )



