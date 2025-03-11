from sqlmodel import Field, SQLModel


class BranchCategoryLink(SQLModel, table=True):
    category_id: int | None = Field(default=None, foreign_key="category.id", primary_key=True)
    branch_id: int | None = Field(default=None, foreign_key="branch.id", primary_key=True)
    priority: int = Field(default=None)