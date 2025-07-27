from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn
from src.core.config import settings
from src.crawl_api.api import router_post

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     yield

# app = FastAPI(lifespan=lifespan)

app = FastAPI()

app.include_router(router_post)

def main():
    uvicorn.run("main:app", host=settings.APP_HOST, port=settings.APP_PORT, reload=True)

if __name__ == "__main__":
    main()

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI + Poetry!"}