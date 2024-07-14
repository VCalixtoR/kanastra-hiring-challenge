"""
Route: 
    - GET /health (APIKey authentication)
Description: 
    - Used for testing the base URL
"""
from fastapi import Depends, APIRouter
from fastapi.responses import JSONResponse
from handlers import auth_with_api_key

router = APIRouter()

@router.get("/health", dependencies=[Depends(auth_with_api_key)])
async def get_health():
    return JSONResponse(content={})