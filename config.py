import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "fastapi_auth")

SECRET_KEY = os.getenv("SECRET_KEY", "supersecret")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

SCHEMA = "http"
HOST = "0.0.0.0"
PORT = 9000

if HOST == "0.0.0.0":
    BASE_URL = f"{SCHEMA}://127.0.0.1:{PORT}"
else: 
    BASE_URL = f"{SCHEMA}://{HOST}:{PORT}" 

AUTH_PREFIX = "/auth"
ADMIN_PREFIX = "/admin"
APIV1_PREFIX = "/api/v1"
