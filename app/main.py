from fastapi import Depends, FastAPI
from sqlmodel import Field, Session, SQLModel, create_engine, select
from app.model.branch_category_product import BranchCategoryProduct
from app.model.branch_category import BranchCategory
from app.model.branch import Branch
from app.model.category import Category
from app.model.history import History, ProductHistory
from app.model.product import Product

from app.routers import branch, category, history, product, auth

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
app.include_router(auth.router)
app.include_router(category.router)
app.include_router(product.router)

@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}