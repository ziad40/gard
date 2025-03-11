from fastapi import Depends, FastAPI
from sqlmodel import Field, Session, SQLModel, create_engine, select
from fastapi import Depends, HTTPException, Query
from typing import Annotated
from .model.branch_category_product import BranchCategoryProductLink
from .model.branch_category import BranchCategoryLink
from .model.branch import Branch
from .model.category import Category
from .model.history import History, ProductHistory
from .model.product import Product

from .routers import branch, category, product, stock

import os
from dotenv import load_dotenv

load_dotenv()

# Database credentials
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_PORT = os.getenv('MYSQL_PORT')
MYSQL_DB = os.getenv('MYSQL_DB')

# SQLModel connection URL
mysql_url = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"

# Create engine
engine = create_engine(mysql_url, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


app.include_router(branch.router)

@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}