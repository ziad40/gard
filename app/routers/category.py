from fastapi import APIRouter, Response, HTTPException
from app.dependencies import BranchDep, SessionDep
from app.service.branch import BranchService
from typing import List
from app.model.branch_category import BranchCategory
from pydantic import BaseModel

router = APIRouter(
        prefix="/branch/category",
        tags=["category"]
    )

class updateCategoryOrderRequest(BaseModel):
    category_ids: List[int]

@router.get("/")
def get_categories_in_branch(branch : BranchDep, session : SessionDep):
    branch_service = BranchService(branch, session)
    categories : List[BranchCategory] = branch_service.get_categries()
    return [
        {
            "category_id": bc.category_id,
            "category_name": bc.category.name,
            "priority": bc.priority,
        }
        for bc in categories
    ]

@router.put("/update-order")
def update_category_order(request : updateCategoryOrderRequest, branch : BranchDep, session : SessionDep):
    branch_service = BranchService(branch, session)
    try:
        branch_service.update_category_order(request.category_ids)
        return Response(status_code=204)  # No content on success
    except ValueError as e:  
        raise HTTPException(status_code=400, detail=str(e))