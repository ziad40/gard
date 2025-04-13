from fastapi import APIRouter, File, UploadFile, Form, HTTPException
from app.dependencies import BranchDep, SessionDep
from app.service.inventory import InventoryService
from pydantic import BaseModel
from app.model.history import History
from typing import List, Optional
router = APIRouter()

router = APIRouter(
        prefix="/branch",
        tags=["branch"]
    )

class newHistoryRequest(BaseModel):
    category_id: int

class NextProductRequest(BaseModel):
    inventory_id: int
    prev_product_id: Optional[int] = None
    prev_product_count_stock: Optional[int] = None
    prev_product_current_count: Optional[int] = None
    state: Optional[str] = None


@router.post("/start-inventory", description="Branch start inventory operation for some category and get a new inventory with id to process stock")
def start(request: newHistoryRequest, branch : BranchDep, session : SessionDep ):
    inv_service = InventoryService(branch, session)
    history : History= inv_service.start_inventory(request.category_id)
    return {
        "inventory_id": history.id,
        "start_date": history.created_at,
        "category_id": history.category_id,
        "category_name": history.category.name
    }


@router.post("/category/next-product", description="The most important endpoint where it process inventory process "
"-- it fetch next product from stock to process stock "
"-- if it is first product in category, then endpoint return the next product"
"-- otherwise user should provide previous product details like current quantity in branch and quantity from stock (which I provide) and image of product."
"-- and state of product (you can treat it as notes about product)"
"--")
def next_product(
    branch : BranchDep,
    session : SessionDep,
    inventory_id: int = Form(...),
    prev_product_id: Optional[int] = Form(None),
    prev_product_count_stock: Optional[int] = Form(None),
    prev_product_current_count: Optional[int] = Form(None),
    state: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None)
):
    request = NextProductRequest(
        inventory_id=inventory_id,
        prev_product_id=prev_product_id,
        prev_product_count_stock=prev_product_count_stock,
        prev_product_current_count=prev_product_current_count,
        state=state
    )

    # Validate that either all optional params are provided or none of them
    optional_params = [prev_product_id, prev_product_count_stock, prev_product_current_count, image, state]
    
    if any(param is not None for param in optional_params) and not all(param is not None for param in optional_params):
        raise HTTPException(status_code=400, detail="Either provide all optional parameters (prev_product_id, prev_product_count_stock, prev_product_current_count, state, image) or none.")


    inv_service = InventoryService(branch, session)
    try:
        product = inv_service.get_next_product_in_category(request, image)

        if not product:
            return {"message": "No more products in this category not processed"}

        return {
            "product_id": product.product_id,
            "product_name": product.product.name,
            "product_quantity": product.quantity,
            "priority": product.priority
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get('/category/current-product', description="this endpoint is used to fetch the current product that needs to be processed"
"it should NOT be used in normal operation"
"-- we use it in case of any problem happen or interruptions of internet lose connection while processing"
"-- so it is used to know where we have stopped")
def current_product(branch : BranchDep, session : SessionDep, inventory_id: int):
    inv_service = InventoryService(branch, session)
    try:
        product = inv_service.get_current_product_in_category(inventory_id)
        if not product:
            return None
        return {
            "product_id": product.product_id,
            "product_name": product.product.name,
            "product_quantity": product.quantity,
            "priority": product.priority
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get('/inventory/unfinished', description="fetch all unfinished inventory that have not completed and we USE current-product end-product to know where to continue the process")
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
