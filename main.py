from src.auth import app_factory
from src.auth.api.v1 import user as api_v1_user
from fastapi import FastAPI

app: FastAPI = app_factory.create(
    title="Auth app",
    version="1.0.0",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
    routers=(
        api_v1_user.router,
    )
)
