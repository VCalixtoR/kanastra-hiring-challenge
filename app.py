from fastapi import FastAPI
from routes.docs import router as DocsRouter
from routes.index import router as IndexRouter
from routes.health import router as HealthRouter
from routes.process_file import router as ProcessFileRouter

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)

# Base routes
app.include_router(DocsRouter)
app.include_router(IndexRouter)
app.include_router(HealthRouter)

# API specific routes
app.include_router(ProcessFileRouter)