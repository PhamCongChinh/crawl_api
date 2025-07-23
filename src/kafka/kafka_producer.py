from aiokafka import AIOKafkaProducer
import asyncio
import json
from kafka.admin import KafkaAdminClient, NewTopic
from src.core.config import settings

producer: AIOKafkaProducer | None = None

async def start_producer():
    global producer
    if not producer:
        producer = AIOKafkaProducer(
            # bootstrap_servers="222.252.32.106:9092"
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



async def create_kafka_topic(topic_name: str):
    admin_client = KafkaAdminClient(bootstrap_servers=f"{settings.KAFKA_BROKER_HOST}:{settings.KAFKA_BROKER_PORT}", client_id="kafka-topic-post")

    topic = NewTopic(
        name=topic_name,
        num_partitions=1,
        replication_factor=1,
    )

    try:
        admin_client.create_topics([topic])
        print(f"Created topic: {topic_name}")
    except Exception as e:
        print(f"Topic '{topic_name}' may already exist or failed: {e}")
    finally:
        admin_client.close()
