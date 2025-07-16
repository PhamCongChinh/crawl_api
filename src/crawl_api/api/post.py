from fastapi import APIRouter, BackgroundTasks, Body, status
from fastapi.responses import JSONResponse
from crawl_api.services.post import PostService
from src.core.mongo import db

router = APIRouter(prefix="/api/v1/posts", tags=["Post"])

@router.get("/")
async def get_videos(limit: int = 2):
    videos = await db["sls_etl_orgs"].find().to_list(length=limit)
    data = [serialize_doc(u) for u in videos]
    return JSONResponse(status_code=status.HTTP_200_OK, content=data)

def serialize_doc(doc: dict):
    doc["id"] = str(doc["_id"])
    del doc["_id"]
    return doc

@router.post("/insert-posts")
async def insert_posts(request: dict):
    return await PostService.insert_posts(items=request)
    # bg_tasks.add_task(PostService.insert_posts, request)
    # return {"message": "Upsert task đã gửi đi"}

@router.post("/insert-unclassified-org-posts")
async def insert_posts(request: dict):
    return await PostService.insert_unclassified_org_posts(items=request)
    # bg_tasks.add_task(PostService.insert_unclassified_org_posts, request)
    # return {"message": "Upsert task đã gửi đi"}