from fastapi import UploadFile
from app.model.branch import Branch
from app.model.history import History, ProductHistory
from app.model.branch_category import BranchCategory
from app.model.branch_category_product import BranchCategoryProduct
from app.model.product import Product
from sqlmodel import Session, select, case, and_, update
from typing import List, TYPE_CHECKING
import shutil
import os
from dotenv import load_dotenv

load_dotenv()

if TYPE_CHECKING:
    from app.routers.branch import NextProductRequest


class InventoryService:
    def __init__(self, branch : Branch, session : Session):
        self.branch = branch
        self.session = session
    
    def start_inventory(self, category_id : int):
        # Check if category exists in the branch
        branch_category = self.session.exec(
            select(BranchCategory).where(
                and_(
                    BranchCategory.branch_id == self.branch.id,
                    BranchCategory.category_id == category_id
                )
            )
        ).first()
        
        if not branch_category:
            raise ValueError("Category not found in the branch")
        
        history = History(branch_id=self.branch.id, category_id=category_id, next_product_order=1)
        self.session.add(history)
        self.session.commit()
        self.session.refresh(history)
        return history
    def get_next_product_in_category(self, request:"NextProductRequest", image : UploadFile):
        history:History = self.session.exec(
            select(History).where(
                History.id == request.iventory_id
            )
        ).first()

        if not history:
            return None
        
        product:BranchCategoryProduct = self.session.exec(
            select(BranchCategoryProduct).where(
                and_(
                    BranchCategoryProduct.branch_category_branch_id == self.branch.id,
                    BranchCategoryProduct.branch_category_category_id == history.category_id,
                    BranchCategoryProduct.priority == history.next_product_order
                )
            )
        ).first()

        history.next_product_order += 1
        if request.prev_product_id is not None:
            new_product_history = ProductHistory(product_id=request.prev_product_id,
                                                 history_id=history.id,
                                                 stock_count=request.prev_product_count_stock,
                                                 real_count=request.prev_product_current_count)
            self.session.add(new_product_history)
            self.session.flush()
            if image:
                path = self.__store_file(image, new_product_history.id)
                new_product_history.image = path

        self.session.commit()
        return product


    def get_unfinished_inventory(self):
        res = self.session.exec(
            select(History)
            .where(and_(
                    History.next_product_order != -1,
                    History.branch_id == self.branch.id
                ))
            ).all()
        return res
    
    def __store_file(self, image: UploadFile, image_id:int) -> str:
        """Save file to disk and return the file's accessible URL"""
        image_name = str(image_id) + "_" + image.filename
        file_path = os.path.join("uploads", image_name)

        # Save file to disk
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

        # Return the full URL
        return file_path

    
    
    
        
