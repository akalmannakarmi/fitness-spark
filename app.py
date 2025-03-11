from fastapi import FastAPI
from auth.routes import router as authRouter
from stats.routes import router as statsRouter
from admin.routes import router as adminRouter
from appV1.routes import router as appV1Router
from config import AUTH_PREFIX,STATS_PREFIX,ADMIN_PREFIX,APIV1_PREFIX

app = FastAPI()

@app.get("/",tags=["Root"])
async def root():
    return {"message":"Welcome to fitness spark"}


app.include_router(authRouter, tags=["Auth"], prefix=AUTH_PREFIX)
app.include_router(statsRouter, tags=["Stats"], prefix=STATS_PREFIX)
app.include_router(adminRouter, tags=["Admin"], prefix=ADMIN_PREFIX)
app.include_router(appV1Router, tags=["V1"], prefix=APIV1_PREFIX)
