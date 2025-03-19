from fastapi import APIRouter
from app.dependencies import SessionDep, BranchDep
from app.service.branch import BranchService
from typing import List
from app.model.branch_category_product import BranchCategoryProduct

router = APIRouter(
        prefix="/branch/category/product",
        tags=["products"]
    )

@router.get("/")
def get_products_in_category_in_branch(category_id: int, branch : BranchDep, session : SessionDep):
    branch_service = BranchService(branch, session)
    products : List[BranchCategoryProduct] = branch_service.get_products(category_id=category_id)
    return [
        {
            "product_id": p.product_id,
            "product_name": p.product.name,
            "product_quantity" : p.quantity,
            "priority": p.priority,
        }
        for p in products
    ]

@router.put("/update-order")
def update_product_order(category_id: int, product_ids: List[int], branch : BranchDep, session : SessionDep):
    branch_service = BranchService(branch, session)
    branch_service.update_products_order_in_category(category_id, product_ids)
    return {"message": "Categories order updated successfully"}