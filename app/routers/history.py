from fastapi import APIRouter, HTTPException
from app.dependencies import BranchDep, SessionDep
from app.service.inventory import InventoryService
from typing import List
from app.model.history import History, ProductHistory
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(
        prefix="/history",
        tags=["history"]
    )

@router.get('/', description="fetch all inventories related to branch with overview details (id, start time, category, status, last product (if inventory is not finished))")
def get_all_histories(branch: BranchDep, session: SessionDep):
    inv_service = InventoryService(branch, session)
    histories : List[History] = inv_service.get_branch_history()
    return [
                {
                    "inventory_id": history.id,
                    "start_date": history.created_at,
                    "category_id": history.category_id,
                    "category_name": history.category.name,
                    "status": "Done" if history.next_product_order == -1 else "Unfinished",
                    **(
                        {
                            "product_id": history.prev_product_id,  
                            "product_name": history.prev_product.name  
                        }
                        if history.next_product_order != -1 else {}
                    ) 
                }
                for history in histories
            ]

@router.get('/details', description="fetch specific information about inventory and what has happened in it for all its products (HISTORY of process)")
def details(branch: BranchDep, session: SessionDep, inventory_id:int):
    inv_service = InventoryService(branch, session)
    try:
        products_history : List[ProductHistory] = inv_service.get_inventory_details(inventory_id)
        return [
                    {
                        "product_id": product_history.product_id,
                        "product_name": product_history.product.name,
                        "stock_count" : product_history.stock_count,
                        "current_count" : product_history.real_count,
                        "state": product_history.state,
                        "image": os.getenv('BASE_URL') + product_history.image
                    }
                for product_history in products_history
        ]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))