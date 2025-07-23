from aiokafka import AIOKafkaProducer
import asyncio
import json
from src.core.config import settings

producer: AIOKafkaProducer | None = None

async def start_producer():
    global producer
    if not producer:
        producer = AIOKafkaProducer(
            # bootstrap_servers="192.168.1.28:9092"
            bootstrap_servers=f"{settings.KAFKA_BROKER_HOST}:{settings.KAFKA_BROKER_PORT}"
        )
        await producer.start()

async def stop_producer():
    global producer
    if producer:
        await producer.stop()

async def send_kafka_message(topic: str, messages: list[dict]):
    if not producer:
        raise Exception("Kafka producer chưa khởi tạo.")

    tasks = [
        producer.send(topic, json.dumps(msg, ensure_ascii=False).encode("utf-8"))
        for msg in messages
    ]

    results = await asyncio.gather(*tasks, return_exceptions=True)

    for i, result in enumerate(results):
        if isinstance(result, Exception):
            print(f"[Kafka] Lỗi khi gửi message {i}: {result}")
    await producer.flush()
