import logging
from datetime import datetime
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from .config import MONGODB_URL, MAX_CONNECTIONS_COUNT, MIN_CONNECTIONS_COUNT
from .models import Todo
from .utils import publish_event

logger = logging.getLogger('app-logger')

class DataBase:
    client: AsyncIOMotorClient = None
    
db = DataBase()


async def get_database() -> AsyncIOMotorClient:
    return db.client


async def connect_to_mongo():
    logger.info("Connecting to Mongo...")
    db.client = AsyncIOMotorClient(MONGODB_URL, maxPoolSize=MAX_CONNECTIONS_COUNT, minPoolSize=MIN_CONNECTIONS_COUNT)
    logger.info("Connected to Mongo")


async def close_mongo_connection():
    logger.info("Closing Mongo...")
    db.client.close()
    logger.info("Closed Mongo")


async def fetch_one_todo(id):
    document = await db.client.expenses_manager.items.find_one({"_id": ObjectId(id)})
    return document


async def fetch_all_todos():
    todos = []
    cursor = db.client.expenses_manager.items.find({})
    async for document in cursor:
        todos.append({**Todo(**document).dict(), "id": str(document['_id'])})
    return todos


async def create_todo(todo):
    document = await db.client.expenses_manager.items.find_one({"title": todo['title']})
    if not document:
        document = todo
        document['created_at'] = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        result = await db.client.expenses_manager.items.insert_one(document)
        await publish_event({**document, "_id": str(result.inserted_id), "type": "add"})
    return document


async def update_todo(id, status):
    await db.client.expenses_manager.items.update_one({"_id": ObjectId(id)}, {"$set": {"hidden": status}})
    document = await db.client.expenses_manager.items.find_one({"_id": ObjectId(id)})
    await publish_event({**document, "_id": id, "type": "update"})
    return document


async def remove_todo(id):
    document = await db.client.expenses_manager.items.find_one({"_id": ObjectId(id)})
    await db.client.expenses_manager.items.delete_one({"_id": ObjectId(id)})
    await publish_event({**document, "_id": id, "type": "delete"})
    return True
