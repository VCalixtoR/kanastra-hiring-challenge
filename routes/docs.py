"""
Routes:
    - GET /docs          (Basic authentication)
    - GET /openapi.json  (Basic authentication)
Description: 
    - Used to view the API documentation (swagger)
"""
from fastapi import Depends, Request, APIRouter
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.routing import APIRoute
from handlers import auth_with_basic_credentials

router = APIRouter()

@router.get("/docs", dependencies=[Depends(auth_with_basic_credentials)])
async def get_documentation():
    """Provides the documentation at the /docs endpoint based on the OpenAPI template returned by the /openapi.json endpoint"""
    return get_swagger_ui_html(openapi_url="/openapi.json", title="docs")

@router.get("/openapi.json", dependencies=[Depends(auth_with_basic_credentials)])
async def get_openapi_json(request: Request):
    """Provides the openapi.json with the documentation of selected routes"""

    # Only document the selected routes
    selected_api_routes = [
        item for item in request.app.routes if isinstance(item, APIRoute) and not item.path in ["/docs", "/openapi.json"]
    ]

    return get_openapi(title="FastAPI", version="0.1.0", routes=selected_api_routes)