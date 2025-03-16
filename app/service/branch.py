from app.model.branch import Branch
from app.model.branch_category import BranchCategory
from app.model.branch_category_product import BranchCategoryProduct
from sqlmodel import Session, select, case, and_
from typing import List

class BranchService:
    def __init__(self, branch : Branch, session : Session):
        self.branch = branch
        self.session = session

    def get_categries(self):
        result = self.session.exec(
            select(BranchCategory)
            .where(BranchCategory.branch_id == self.branch.id)
            .order_by(
                case((BranchCategory.priority == None, 1), else_=0),
                BranchCategory.priority
                ) 
        )
        branch_categories:List[BranchCategory] = result.all()

        # Separate categories into those with and without priority
        categories_with_priority:List[BranchCategory] = [bc for bc in branch_categories if bc.priority is not None]
        categories_without_priority:List[BranchCategory] = [bc for bc in branch_categories if bc.priority is None]

        # Find maximum priority from existing ones (default to 0 if none)
        max_priority = max([bc.priority for bc in categories_with_priority], default=0)

        # Assign new priorities to categories without priority
        for bc in categories_without_priority:
            max_priority += 1  # Increment priority
            bc.priority = max_priority  # Assign new priority

        # Commit updates to the database
        if categories_without_priority:
            self.session.commit()

        return categories_with_priority + categories_without_priority
    
    
