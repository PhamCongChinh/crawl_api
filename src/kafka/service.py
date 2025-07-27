from confluent_kafka.admin import AdminClient, NewTopic
from confluent_kafka import Producer
import logging
from src.core.config import settings

# Config Kafka
KAFKA_BOOTSTRAP_SERVERS = f"{settings.KAFKA_BROKER_HOST}:{settings.KAFKA_BROKER_PORT}"

# --- Kafka clients -------------------------------------------------
admin = AdminClient({"bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS})
producer = Producer({"bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS})


def create_topic_if_not_exists(topic_name: str):
    """Tạo Kafka topic nếu chưa có."""
    metadata = admin.list_topics(timeout=5)

    if topic_name in metadata.topics:
        return  # đã có → bỏ qua

    topic = NewTopic(topic=topic_name, num_partitions=1, replication_factor=1)
    fs = admin.create_topics([topic])

    try:
        fs[topic_name].result()  # chờ topic tạo xong
        logging.info(f"Đã tạo topic: {topic_name}")
    except Exception as e:
        if "TopicAlreadyExistsError" in str(e):
            pass  # nếu vừa có thằng khác tạo thì bỏ qua lỗi này
        else:
            raise Exception(f"Lỗi khi tạo topic '{topic_name}': {e}")