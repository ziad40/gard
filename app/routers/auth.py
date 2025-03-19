from fastapi import APIRouter, Depends, HTTPException, Response
from pydantic import BaseModel
from app.service.auth import AuthService
from app.dependencies import SessionDep, BranchDep


router = APIRouter(
    prefix="/auth",
    tags=["authentication"],)

class LoginRequest(BaseModel):
    password: str
    code: str
class RegisterRequest(LoginRequest):
    branchname: str


@router.post("/register")
def register(request: RegisterRequest, db: SessionDep):
    try:
        branch, token = AuthService.register(db, request.branchname, request.password, request.code)
        return {"branch id": branch.id, "token" : token}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.post("/login")
def login(request: LoginRequest, db: SessionDep):
    try:
        branch, token = AuthService.login(db, request.password, request.code)
        return {"branch id": branch.id,"branch name" : branch.name,  "token" : token}
    except HTTPException as e:
        raise e

@router.get('/auth')
def auth(branch: BranchDep):
    token = AuthService.create_access_token(branch.id, branch.name)
    return {"branch id": branch.id,"branch name" : branch.name,  "token" : token}