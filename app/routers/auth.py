from fastapi import APIRouter, Depends, HTTPException, Response
from pydantic import BaseModel
from app.service.auth import AuthService
from app.dependencies import SessionDep, BranchDep


router = APIRouter(
    prefix="/auth",
    tags=["authentication"]
)

class LoginRequest(BaseModel):
    password: str
    code: str
class RegisterRequest(LoginRequest):
    branchname: str


@router.post("/register", include_in_schema=False, description="Creates a new branch and returns an authentication token.")
def register(request: RegisterRequest, db: SessionDep):
    try:
        branch, token = AuthService.register(db, request.branchname, request.password, request.code)
        return {"branch id": branch.id, "token" : token}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.post("/login", description="Logs in a branch and returns an authentication token to use in further requests and get data related to current (logged) branch")
def login(request: LoginRequest, db: SessionDep):
    try:
        branch, token = AuthService.login(db, request.password, request.code)
        return {"branch id": branch.id,"branch name" : branch.name,  "token" : token}
    except HTTPException as e:
        raise e

@router.get('/auth', description="Returns a new authentication token for an already authenticated branch.")
def auth(branch: BranchDep):
    token = AuthService.create_access_token(branch.id, branch.name)
    return {"branch id": branch.id,"branch name" : branch.name,  "token" : token}