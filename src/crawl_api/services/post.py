from fastapi import HTTPException
from pydantic import ValidationError
from pymongo import UpdateOne
from crawl_api.models.post_classified import PostClassifiedModel
from crawl_api.models.post_unclassified import PostUnclassifiedModel
from src.core.mongo import db
import logging

class PostService():
    @staticmethod
    async def insert_posts(items: dict):
        operations = []
        for item in items.get("data"):
            try:
                post = PostClassifiedModel(**item)  # validate với Pydantic
                logging.info("Dữ liệu hợp lệ:", post.model_dump().get("url"))
                data = post.model_dump()
                operations.append(
                    UpdateOne(
                        {"url": post.url},      # dùng luôn field đã được validate
                        {"$set": data},
                        upsert=True
                    )
                )
            except ValidationError as e:
                logging.error("Bỏ qua item không hợp lệ:")
                logging.error(e.json(indent=2))
        if operations:
            result = await db["data_classified"].bulk_write(operations, ordered=False)
            return {
                "matched": result.matched_count,
                "modified": result.modified_count,
                "upserted": len(result.upserted_ids),
            }
        return {"msg": "No valid operations"}

    @staticmethod
    async def insert_unclassified_org_posts(items: dict):
        operations = []
        for item in items.get("data"):
            try:
                post = PostUnclassifiedModel(**item)  # validate với Pydantic
                logging.info("Dữ liệu hợp lệ:", post.model_dump().get("url"))
                data = post.model_dump()
                operations.append(
                    UpdateOne(
                        {"url": post.url},      # dùng luôn field đã được validate
                        {"$set": data},
                        upsert=True
                    )
                )
            except ValidationError as e:
                logging.error("Bỏ qua item không hợp lệ:")
                logging.error(e.json(indent=2))
        if operations:
            result = await db["data_unclassified"].bulk_write(operations, ordered=False)
            return {
                "matched": result.matched_count,
                "modified": result.modified_count,
                "upserted": len(result.upserted_ids),
            }
        return {"msg": "No valid operations"}