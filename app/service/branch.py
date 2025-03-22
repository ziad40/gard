from app.model.branch import Branch
from app.model.branch_category import BranchCategory
from app.model.branch_category_product import BranchCategoryProduct
from sqlmodel import Session, select, case, and_, update, func
from typing import List
from app.service.inventory import InventoryService

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
    
    def update_category_order(self, category_ids:List[int]):
        try:
            self.session.exec(
                update(BranchCategory).values(priority = None)
            )
            for i, category_id in enumerate(category_ids, start=1):
                self.session.exec(
                    update(BranchCategory).where(
                        and_(
                            BranchCategory.branch_id == self.branch.id,
                            BranchCategory.category_id == category_id
                        )
                    ).values(priority=i)
                )
            self.session.commit()
        except ValueError as e:
            raise e

    
    def update_products_order_in_category(self, category_id:int, product_ids:List[int]):
        try:
            inventory_service = InventoryService(self.branch, self.session)
            if len(inventory_service.get_unfinished_inventory_in_categoty(category_id)) != 0:
                raise ValueError("Cannot update category order while there are unfinished inventories")
            
            if self.count_branch_category_products(category_id) != len(product_ids):
                raise ValueError("Number of products in the category does not match the provided list")
            
            current_product_ids = self.get_product_ids(category_id)
            if set(current_product_ids) != set(product_ids):
                raise ValueError("Provided product IDs do not match the current product IDs in the category")
            
            self.session.exec(
                update(BranchCategoryProduct).where(
                    and_(
                            BranchCategoryProduct.branch_category_branch_id == self.branch.id,
                            BranchCategoryProduct.branch_category_category_id == category_id
                        )
                    ).values(priority = None)
            )
            for i, product_id in enumerate(product_ids, start=1):
                self.session.exec(
                    update(BranchCategoryProduct).where(
                        and_(
                            BranchCategoryProduct.branch_category_branch_id == self.branch.id,
                            BranchCategoryProduct.branch_category_category_id == category_id,
                            BranchCategoryProduct.product_id == product_id
                        )
                    ).values(priority=i)
                )
            self.session.commit()
        except ValueError as e:
            raise e
        
    def get_product_ids(self, category_id: int):
        query = select(BranchCategoryProduct.product_id).where(
            BranchCategoryProduct.branch_category_branch_id == self.branch.id,
            BranchCategoryProduct.branch_category_category_id == category_id
        )
        return self.session.exec(query).all()  # Fetch all product IDs
    
    def count_branch_category_products(self, category_id: int):
        count_query = select(func.count()).where(
            BranchCategoryProduct.branch_category_branch_id == self.branch.id,
            BranchCategoryProduct.branch_category_category_id == category_id
        )
        return self.session.exec(count_query).one()  # Fetch the count

    
