"""
    Module that configures authentication via Basic Credentials or API Key, use dependencies=[Depends(auth_with_basic_credentials)] or 
        dependencies=[Depends(auth_with_api_key)] in the arguments to authenticate the route
"""
import secrets
from fastapi import Depends, HTTPException, Security, status
from fastapi.security import APIKeyHeader, HTTPBasic, HTTPBasicCredentials
from providers import injector_container, IEnvironmentHandler

http_basic = HTTPBasic()
def auth_with_basic_credentials(credentials: HTTPBasicCredentials = Depends(http_basic)):
    """Configures basic authentication to verify documentation access"""

    env_handler: IEnvironmentHandler = injector_container.get(IEnvironmentHandler)

    correct_username = secrets.compare_digest(credentials.username, env_handler.getenv("DOCS_USERNAME"))
    correct_password = secrets.compare_digest(credentials.password, env_handler.getenv("DOCS_PASSWORD"))

    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    
    return credentials.username

api_key_header = APIKeyHeader(name="x-api-key", auto_error=False)
def auth_with_api_key(api_key: str = Security(api_key_header)):
    """
        Allows authentication of specific API routes via API_KEY
        Configure the Authorization header with the respective key and value before querying the API
    """

    env_handler: IEnvironmentHandler = injector_container.get(IEnvironmentHandler)

    if api_key != env_handler.getenv("API_KEY"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing api_key",
        )