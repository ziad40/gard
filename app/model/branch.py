from sqlmodel import Field, SQLModel, Relationship
from app.model.category import Category
from app.model.branch_category import BranchCategoryLink


class Branch(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    code: str = Field(index=True)
    password: str = Field(default=None)

    categories: list["Category"] = Relationship(link_model=BranchCategoryLink)




