from sqlmodel import Session, create_engine, select
from typing import Annotated
import jwt
from fastapi import Depends, HTTPException, status
from jwt.exceptions import InvalidTokenError
from app.model.branch import Branch
import os
from dotenv import load_dotenv
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

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


def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

security = HTTPBearer()

def get_current_token(token: HTTPAuthorizationCredentials = Depends(security)):
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is required",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token.credentials

TokenDep = Annotated[str, Depends(get_current_token)]

async def get_current_branch(token: TokenDep, session: SessionDep):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=[os.getenv('ALGORITHM')])
        branch_name = payload.get("branch_name")
        branch_id = payload.get("branch_id")
        if branch_name is None or branch_id is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    branch = session.get(Branch, branch_id)
    if branch is None:
        raise credentials_exception
    return branch

BranchDep = Annotated[Branch, Depends(get_current_branch)]
