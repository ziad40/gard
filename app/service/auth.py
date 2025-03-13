import jwt
import bcrypt
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from sqlmodel import Session, select, or_, and_
from app.model.branch import Branch
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

load_dotenv()

class AuthService:
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
    
    @staticmethod
    def hash_password(password: str) -> str:
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    @staticmethod
    def create_access_token(branch_id: int, branch_name: str) -> str:
        payload = {
            "branch_name": branch_name,
            "branch_id": branch_id,
            "exp": datetime.utcnow() + timedelta(weeks=54)
        }
        return jwt.encode(payload, key=os.getenv('SECRET_KEY'), algorithm=os.getenv('ALGORITHM'))

    @staticmethod
    def register(session: Session, branch_name: str, password: str, code: str):
        
        statement = select(Branch).where(
        or_(Branch.name == branch_name, Branch.code == code)
        )
        result = session.exec(statement).first()
        if result:
            raise ValueError("Username or code already exists")
        
        hashed_password = AuthService.hash_password(password)
        new_branch = Branch(name=branch_name, password=hashed_password, code=code)

        try:
            session.add(new_branch)
            session.commit()
            session.refresh(new_branch)
            return new_branch, AuthService.create_access_token(new_branch.id, new_branch.name)
        except IntegrityError:
            session.rollback()
            raise ValueError("Database integrity error: Username or code may already exist")
        
    
    @staticmethod
    def login(session: Session, password: str, code: str):
        statement = select(Branch).where(Branch.code == code)
        branch = session.exec(statement).first()

        if not branch or not AuthService.verify_password(password, branch.password):
            raise HTTPException(status_code=401, detail="Wrong Credentials")
        
        return branch, AuthService.create_access_token(branch.id, branch.name)
    
    
        


