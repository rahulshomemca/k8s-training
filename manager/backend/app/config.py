import os
import asyncio

loop = asyncio.get_event_loop()

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://root:rootpassword@localhost/?authMechanism=DEFAULT")
MAX_CONNECTIONS_COUNT = int(os.getenv("MAX_CONNECTIONS_COUNT", 10))
MIN_CONNECTIONS_COUNT = int(os.getenv("MIN_CONNECTIONS_COUNT", 10))
PROJECT_NAME = os.getenv("PROJECT_NAME", "API Documentation")

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9093")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "expenses")
KAFKA_CONSUMER_GROUP = os.getenv("KAFKA_CONSUMER_GROUP", "group-id")