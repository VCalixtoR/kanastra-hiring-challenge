"""
Route: 
    - POST /process-file (APIKey authentication)
Description: 
    - Performs file processing
"""
from fastapi import Depends, APIRouter
from core import ProcessFile
from handlers import auth_with_api_key

router = APIRouter()

@router.post("/process-file", dependencies=[Depends(auth_with_api_key)])
async def post_process_file():
    return await ProcessFile().execute()