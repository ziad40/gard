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
        branch_category_product:BranchCategoryProduct = self.session.exec(
            select(BranchCategoryProduct).where(
                and_(
                    BranchCategoryProduct.branch_category_branch_id == self.branch.id,
                    BranchCategoryProduct.branch_category_category_id == category_id,
                    BranchCategoryProduct.priority == 1
                )
            )
        ).first()
        if not branch_category_product:
            raise ValueError("Category not found in the branch")
        history = History(branch_id=self.branch.id, category_id=category_id, next_product_order=1,
                           prev_product_id=branch_category_product.product_id)
        self.session.add(history)
        self.session.commit()
        self.session.refresh(history)
        return history
    def get_next_product_in_category(self, request:"NextProductRequest", image : UploadFile):
        history:History = self.session.exec(
            select(History).where(
                History.id == request.inventory_id
            )
        ).first()

        if not history:
            raise ValueError("No Such Inventory Exists.")
        if request.prev_product_id is None and history.next_product_order != 1:
            raise ValueError("You must provide a previous product details.")
        if request.prev_product_id is not None and history.next_product_order != 1 and history.prev_product_id != request.prev_product_id:
            raise ValueError("Previous product id does not match the one You should provide.")

        product:BranchCategoryProduct = self.session.exec(
            select(BranchCategoryProduct).where(
                and_(
                    BranchCategoryProduct.branch_category_branch_id == self.branch.id,
                    BranchCategoryProduct.branch_category_category_id == history.category_id,
                    BranchCategoryProduct.priority == history.next_product_order
                )
            )
        ).first()

        if not product:
            history.next_product_order = -1
        else:
            history.prev_product_id = product.product_id
            history.next_product_order += 1

        if request.prev_product_id is not None and history.next_product_order != 2:
            new_product_history = ProductHistory(product_id=request.prev_product_id,
                                                 history_id=history.id,
                                                 stock_count=request.prev_product_count_stock,
                                                 real_count=request.prev_product_current_count,
                                                 state = request.state)
            self.session.add(new_product_history)
            self.session.flush()
            if image:
                path = self.__store_file(image, new_product_history.id)
                new_product_history.image = path

        self.session.commit()
        return product

    def get_current_product_in_category(self, inventory_id:int):
        history:History = self.session.exec(
            select(History).where(
                History.id == inventory_id
            )
        ).first()

        if not history:
            raise ValueError("No Such Inventory Exists.")
        return self.session.exec(
            select(BranchCategoryProduct).where(
                and_(
                    BranchCategoryProduct.branch_category_branch_id == self.branch.id,
                    BranchCategoryProduct.branch_category_category_id == history.category_id,
                    BranchCategoryProduct.priority == history.next_product_order-1
                )
            )
        ).first()
        
        
    def get_unfinished_inventory(self):
        res = self.session.exec(
            select(History)
            .where(and_(
                    History.next_product_order != -1,
                    History.branch_id == self.branch.id
                ))
            ).all()
        return res
    
    def get_unfinished_inventory_in_categoty(self, category_id : int):
        res = self.session.exec(
            select(History)
            .where(and_(
                    History.next_product_order != -1,
                    History.branch_id == self.branch.id,
                    History.category_id == category_id
                ))
            ).all()
        print(res)
        return res
    
    def get_branch_history(self):
        return self.session.exec(
            select(History).where(
                History.branch_id == self.branch.id
            )
        ).all()
    
    def get_inventory_details(self, inventory_id):
        history = self.session.exec(
            select(History).where(
                History.id == inventory_id
            )
        ).first()
        if not history or history is not None and history.branch_id != self.branch.id:
            raise ValueError("No Such Inventory Exists.")
        return history.products
    
    def __store_file(self, image: UploadFile, image_id:int) -> str:
        """Save file to disk and return the file's accessible URL"""
        image_name = str(image_id) + "_" + image.filename
        file_path = os.path.join(os.getenv("UPLOADS"), image_name)

        # Save file to disk
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

        # Return the full URL
        return file_path
