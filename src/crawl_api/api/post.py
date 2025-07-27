import json
from fastapi import APIRouter, BackgroundTasks, Body, HTTPException, status
from crawl_api.services.post import PostService
from src.kafka.message import MessagePayload
from src.kafka.service import create_topic_if_not_exists
from src.core.mongo import db
from confluent_kafka import Producer
from src.core.config import settings

producer = Producer({
    'bootstrap.servers': f"{settings.KAFKA_BROKER_HOST}:{settings.KAFKA_BROKER_PORT}"
})

router = APIRouter(prefix="/api/v1/posts", tags=["Post"])

# @router.get("/")
# async def get_videos(limit: int = 2):
#     videos = await db["sls_etl_orgs"].find().to_list(length=limit)
#     data = [serialize_doc(u) for u in videos]
#     return JSONResponse(status_code=status.HTTP_200_OK, content=data)

def serialize_doc(doc: dict):
    doc["id"] = str(doc["_id"])
    del doc["_id"]
    return doc

@router.post("/insert-posts")
async def insert_posts_classified(request: dict): # data là 1 list dict
    try:
        await PostService.insert_posts(items=request)
        topic = "data-classified"
        create_topic_if_not_exists(topic)
        data = request.get("data", [])
        for item in data:
            producer.produce(
                topic=topic,
                value=json.dumps(item).encode('utf-8')
            )

        producer.flush()
        return {"status": "OK", "detail": f"Sent to topic '{topic}'"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    # return {"message": "Upsert task đã gửi đi"}

@router.post("/insert-unclassified-org-posts")
async def insert_posts_unclassified(request: dict):
    try:
        await PostService.insert_unclassified_org_posts(items=request)
        topic = "data-unclassified"
        create_topic_if_not_exists(topic)  # <-- kiểm tra & tạo topic
    
        data = request.get("data", [])
        for item in data:
            producer.produce(
                topic=topic,
                value=json.dumps(item).encode('utf-8')
            )

        producer.flush()
        return {"status": "OK", "detail": f"Sent to topic '{topic}'"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    # return {"message": "Upsert task đã gửi đi"}


@router.post("/send")
def send_to_kafka(request: dict): #data: MessagePayload
    topic = "data-classified"
    create_topic_if_not_exists(topic)  # <-- kiểm tra & tạo topic
    
    data = request.get("data", [])
    for item in data:
        producer.produce(
            topic=topic,
            value=json.dumps(item).encode('utf-8')
        )

    producer.flush()
    return {"status": "OK", "detail": f"Sent to topic '{topic}'"}