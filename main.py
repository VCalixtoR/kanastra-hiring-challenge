"""
    Used locally only with the command: python main.py. In dev/prod, containers are used with the module and variable app:app
    
    For deploying the API, uvicorn is used, which is an ASGI Web server that implements
        production functionalities for the standard API
"""
import os
import uvicorn

# Executed locally: Loads and checks the necessary environments to start the application using defaults in their absence
if __name__ == "__main__":
    uvicorn.run("app:app", host=os.getenv("HOST", "0.0.0.0"), port=int(os.getenv("PORT", "8080")), reload=True)