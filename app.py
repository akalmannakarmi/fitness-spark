from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from appV1.routes import router as app_v1_router
from auth.routes import router as auth_router
from config import APIV1_PREFIX, AUTH_PREFIX, CORS_ORIGINS, STATS_PREFIX
from stats.routes import router as stats_router
from utils.exception import register_exception_handlers

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_exception_handlers(app)


@app.get("/", tags=["Root"])
async def root() -> dict[str, str]:
    return {"message": "Welcome to fitness spark"}


app.include_router(auth_router, tags=["Auth"], prefix=AUTH_PREFIX)
app.include_router(stats_router, tags=["Stats"], prefix=STATS_PREFIX)
app.include_router(app_v1_router, tags=["V1"], prefix=APIV1_PREFIX)
