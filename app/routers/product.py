from fastapi import APIRouter, HTTPException, Response
from app.dependencies import SessionDep, BranchDep
from app.service.branch import BranchService
from typing import List
from app.model.branch_category_product import BranchCategoryProduct
from pydantic import BaseModel
class updateProductOrderRequest(BaseModel):
    category_id: int
    product_ids: List[int]

router = APIRouter(
        prefix="/branch/category/product",
        tags=["products"]
    )

@router.get("", description="fetch all products of specific category in branch, and it order products in random order and continue with this order if user"
"doesn't change order")
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

@router.put("/update-order", description="user can change order of products, by sending his wanted order as list of their IDs")
def update_product_order(request : updateProductOrderRequest, branch : BranchDep, session : SessionDep):
    branch_service = BranchService(branch, session)
    try:
        branch_service.update_products_order_in_category(request.category_id, request.product_ids)
        return Response(status_code=204)  # No content on success
    except ValueError as e:  
        raise HTTPException(status_code=400, detail=str(e))