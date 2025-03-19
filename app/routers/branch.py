from fastapi import APIRouter, File, UploadFile, Form, HTTPException
from app.dependencies import BranchDep, SessionDep
from app.service.inventory import InventoryService
from pydantic import BaseModel
from app.model.history import History
from typing import List, Optional
router = APIRouter()

router = APIRouter(
        prefix="/branch/",
        tags=["products"]
    )

class newHistoryRequest(BaseModel):
    category_id: int

class NextProductRequest(BaseModel):
    iventory_id: int
    prev_product_id: Optional[int] = None
    prev_product_count_stock: Optional[int] = None
    prev_product_current_count: Optional[int] = None


@router.post("/start-inventory")
def start(request: newHistoryRequest, branch : BranchDep, session : SessionDep ):
    inv_service = InventoryService(branch, session)
    history : History= inv_service.start_inventory(request.category_id)
    return {
        "inventory_id": history.id,
        "start_date": history.created_at,
        "category_id": history.category_id,
        "category_name": history.category.name
    }


@router.post("/category/next-product")
def next_product(
    branch : BranchDep,
    session : SessionDep,
    iventory_id: int = Form(...),
    prev_product_id: Optional[int] = Form(None),
    prev_product_count_stock: Optional[int] = Form(None),
    prev_product_current_count: Optional[int] = Form(None),
    image: UploadFile = File(...)
):
    request = NextProductRequest(
        iventory_id=iventory_id,
        prev_product_id=prev_product_id,
        prev_product_count_stock=prev_product_count_stock,
        prev_product_current_count=prev_product_current_count
    )

    # Validate that either all optional params are provided or none of them
    optional_params = [prev_product_id, prev_product_count_stock, prev_product_current_count]
    
    if any(param is not None for param in optional_params) and not all(param is not None for param in optional_params):
        raise HTTPException(status_code=400, detail="Either provide all optional parameters or none.")


    inv_service = InventoryService(branch, session)
    product = inv_service.get_next_product_in_category(request, image)

    if not product:
        return {"message": "No more products in this category not processed"}

    return {
        "product_id": product.product_id,
        "product_name": product.product.name,
        "product_quantity": product.quantity,
        "priority": product.priority
    }


@router.get('/inventory/unfinished')
def get_unfinished_inventories(branch : BranchDep, session : SessionDep):
    inv_service = InventoryService(branch, session)
    unfinished_inventories : List[History] = inv_service.get_unfinished_inventory()
    return [
        {
            "inventory_id": history.id,
            "start_date": history.created_at,
            "category_id": history.category_id,
            "category_name": history.category.name
        }
        for history in unfinished_inventories
    ]
