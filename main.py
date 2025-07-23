from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn
from src.kafka.kafka_producer import create_kafka_topic, start_producer, stop_producer
from src.core.config import settings
from src.crawl_api.api import router_post

@asynccontextmanager
async def lifespan(app: FastAPI):
    # await create_kafka_topic("topic-data-classified")
    # await create_kafka_topic("topic-data-unclassified")
    await start_producer()
    yield
    await stop_producer()

app = FastAPI(lifespan=lifespan)

app.include_router(router_post)

def main():
    uvicorn.run("main:app", host=settings.APP_HOST, port=settings.APP_PORT, reload=True)

if __name__ == "__main__":
    main()

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI + Poetry!"}