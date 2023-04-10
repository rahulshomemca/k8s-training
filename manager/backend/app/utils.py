from aiokafka import AIOKafkaProducer
from json import dumps
import logging
from .config import loop, KAFKA_BOOTSTRAP_SERVERS, KAFKA_TOPIC

logger = logging.getLogger('app-logger')

async def publish_event(message):
    producer = AIOKafkaProducer(
        loop=loop, bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)
    await producer.start()
    try:
        logger.info(f'Sending data with value: {dumps(message)}')
        await producer.send_and_wait(
            topic=KAFKA_TOPIC, 
            value=dumps(message).encode('utf-8')
        )
    finally:
        await producer.stop()