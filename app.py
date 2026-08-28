from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from auth.routes import router as authRouter
from stats.routes import router as statsRouter
from appV1.routes import router as appV1Router
from config import AUTH_PREFIX,STATS_PREFIX,APIV1_PREFIX,CORS_ORIGINS
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

@app.get("/",tags=["Root"])
async def root():
    return {"message":"Welcome to fitness spark"}


app.include_router(authRouter, tags=["Auth"], prefix=AUTH_PREFIX)
app.include_router(statsRouter, tags=["Stats"], prefix=STATS_PREFIX)
app.include_router(appV1Router, tags=["V1"], prefix=APIV1_PREFIX)
