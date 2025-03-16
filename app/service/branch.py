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
        return self.ensure_category_order(branch_categories)
        
    
    def ensure_category_order(self, branch_categories:List[BranchCategory]):
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
    

    def get_products(self, category_id : int):
        branch_category_product = self.session.exec(
            select(BranchCategoryProduct).where(
                and_(
                    BranchCategoryProduct.branch_category_branch_id == self.branch.id,
                    BranchCategoryProduct.branch_category_category_id == category_id
                )
            ).order_by(
                    case((BranchCategoryProduct.priority == None, 1), else_=0),
                    BranchCategoryProduct.priority
                )
        ).all()
        return self.ensure_products_with_priority(branch_category_product)
        
    
    def ensure_products_with_priority(self, branch_category_product : List[BranchCategoryProduct]):
        products_with_priority:List[BranchCategoryProduct] = [bcp for bcp in branch_category_product if bcp.priority is not None]
        products_without_priority:List[BranchCategoryProduct] = [bcp for bcp in branch_category_product if bcp.priority is None]

        # Find maximum priority from existing ones (default to 0 if none)
        max_priority = max([bcp.priority for bcp in products_with_priority], default=0)

        # Assign new priorities to categories without priority
        for bcp in products_without_priority:
            max_priority += 1  # Increment priority
            bcp.priority = max_priority  # Assign new priority

        # Commit updates to the database
        if products_without_priority:
            self.session.commit()

        return products_with_priority + products_without_priority
