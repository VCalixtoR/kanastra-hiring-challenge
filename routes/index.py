"""
Route: 
    - GET / (APIKey authentication)
Description: 
    - Used for testing the base URL
"""
from fastapi import Depends, APIRouter
from handlers import auth_with_api_key

router = APIRouter()

@router.get("/", dependencies=[Depends(auth_with_api_key)])
async def get_index():
    return {"message": "Welcome to the root route of my FastAPI example, feel free to use it in your applications 😃!"}