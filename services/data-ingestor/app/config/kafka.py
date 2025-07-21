from aiokafka import AIOKafkaProducer  # type: ignore

from config.settings import KAFKA_BOOTSTRAP


async def startup_event():
    producer = AIOKafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP,
        acks="all",
        linger_ms=20,              # 20ms
        max_request_size=1048576,  # 1MB
        enable_idempotence=True,
    )
    await producer.start()
    return producer


async def shutdown_event(producer: AIOKafkaProducer = None):
    if producer:
        await producer.stop()
        producer = None
