from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import v1_router
from api.admin_users import router as admin_users_router
from api.auth import router as auth_router
from api.stats import router as stats_router
from config import (
    ADMIN_PREFIX,
    APIV1_PREFIX,
    AUTH_PREFIX,
    CORS_ORIGINS,
    STATS_PREFIX,
)
from exceptions import register_exception_handlers

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)

register_exception_handlers(app)


@app.get("/", tags=["Root"])
async def root() -> dict[str, str]:
    return {"message": "Welcome to fitness spark"}


app.include_router(auth_router, tags=["Auth"], prefix=AUTH_PREFIX)
app.include_router(
    admin_users_router, tags=["Auth"], prefix=f"{AUTH_PREFIX}{ADMIN_PREFIX}"
)
app.include_router(stats_router, tags=["Stats"], prefix=STATS_PREFIX)
app.include_router(v1_router, tags=["V1"], prefix=APIV1_PREFIX)
