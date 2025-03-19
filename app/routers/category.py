from fastapi import APIRouter, Response
from app.dependencies import BranchDep, SessionDep
from app.service.branch import BranchService
from typing import List
from app.model.branch_category import BranchCategory

router = APIRouter(
        prefix="/branch/category",
        tags=["category"]
    )

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
def update_category_order(category_ids: List[int], branch : BranchDep, session : SessionDep):
    branch_service = BranchService(branch, session)
    branch_service.update_category_order(category_ids)
    return Response(status_code=204)