from src.auth.infrastructure import app_factory, di_container_factory
from src.auth.presentation.api.v1 import user as api_v1_user
from fastapi import FastAPI

app: FastAPI = app_factory.create(
    title="Auth app",
    version="1.0.0",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
    routers=(
        api_v1_user.router,
    ),
    di_container_factory=di_container_factory
)
