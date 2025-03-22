from app.dependencies import BranchDep
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

UPLOADS = os.getenv('UPLOADS') # Define base folder

@router.get("/uploads/{media_path:path}")  # Hardcode 'uploads' in the route
def fetch_media(media_path: str, branch: BranchDep):

    # Construct the absolute path to the file
    file_path = UPLOADS + '/' + media_path
    file_path = os.path.normpath(file_path)  # Normalize separators

    # Ensure file exists before returning
    if os.path.exists(file_path) and os.path.isfile(file_path):
        return FileResponse(file_path)

    raise HTTPException(status_code=404, detail="File not found")

