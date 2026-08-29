import uvicorn

from config import HOST, PORT, RELOAD

if __name__ == "__main__":
    uvicorn.run(app="app:app", host=HOST, port=PORT, reload=RELOAD)
