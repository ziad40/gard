from fastapi import Depends, FastAPI
from sqlmodel import Field, Session, SQLModel, create_engine, select
from app.model.branch_category_product import BranchCategoryProduct
from app.model.branch_category import BranchCategory
from app.model.branch import Branch
from app.model.category import Category
from app.model.history import History, ProductHistory
from app.model.product import Product

from app.routers import branch, category, history, product, auth, media

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
UPLOAD_FOLDER = os.getenv("UPLOADS")

@app.on_event("startup")
def on_startup():
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    create_db_and_tables()


app.include_router(branch.router)
app.include_router(auth.router)
app.include_router(category.router)
app.include_router(product.router)
app.include_router(history.router)
app.include_router(media.router)

@app.get("/")
async def root():
    return {
        "message": "Hello, Gard application! You can now access endpoints.",
        "workflow": [
            "1. Login with branch",
            "2. Navigate branch",
            {
                "2.1": "Get branch categories in some order (change order if needed).",
                "2.2": "Get products in each category in some order (change order if needed)."
            },
            "________________________________________________________________",
            "3. Start inventory process",
            {
                "3.1": "Get all categories in branch to start inventory process with each category.",
                "3.2": "Start inventory process for each category.",
                "3.3": "Get products in each category and provide details of each finished product to save data to history."
            },
            "________________________________________________________________",
            "4. Get inventory details (History)",
            {
                "4.1": "Get all history records (finished and unfinished).",
                "4.2": "Get details of each finished product in inventory.",
                "4.3": "Continue unfinished inventory process by fetching the current product endpoint."
            },
            "You can also make it available at the start of the application as a reminder."
        ],
        "docs": "Visit http://34.165.223.128:8000/docs to see API documentation."
    }
