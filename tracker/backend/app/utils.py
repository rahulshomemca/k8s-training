from aiokafka import AIOKafkaConsumer
from json import loads
from .database import add_item, update_item, delete_item
from .config import loop, KAFKA_BOOTSTRAP_SERVERS, KAFKA_CONSUMER_GROUP, KAFKA_TOPIC


async def consume_event():
    consumer = AIOKafkaConsumer(KAFKA_TOPIC, loop=loop,
                                bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS, group_id=KAFKA_CONSUMER_GROUP)
    await consumer.start()
    try:
        async for msg in consumer:
            data = loads(msg.value)
            print(f'Consumer msg: {data}')

            if data['type'] == "add":
                await add_item(data)

            elif data['type'] == "update":
                await update_item(data)
        
            elif data['type'] == "delete":
                await delete_item(data)
    finally:
        await consumer.stop()