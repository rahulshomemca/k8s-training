import logging
import json
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from .config import MONGODB_URL, MAX_CONNECTIONS_COUNT, MIN_CONNECTIONS_COUNT
from .models import Category, Item
from .websocket_manager import WebsocketManager

logger = logging.getLogger('app-logger')

class DataBase:
    client: AsyncIOMotorClient = None
    
db = DataBase()

# websocket manager
ws_manager = WebsocketManager(logger)


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


async def add_item(data):
    document = await db.client.expenses_tracker.category.find_one({"name": data['category']})
    if not document:
        document = Category(
            name=data['category'],
            items={data['_id']: Item(title=data['title'], price=data['price'], hidden=data['hidden'])},
            created_at=datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        )
        await db.client.expenses_tracker.category.insert_one(document.dict())

    elif document:
        if data['_id'] not in document['items'].keys():
            items = {**document['items'], data['_id']: Item(title=data['title'], price=data['price'], hidden=data['hidden']).dict()}
            await db.client.expenses_tracker.category.update_one({"name": data['category']}, {"$set": {"items": items}})
    
    await analytics_data()


async def update_item(data):
    document = await db.client.expenses_tracker.category.find_one({"name": data['category']})
    if document:
        document['items'][data['_id']] = Item(title=data['title'], price=data['price'], hidden=data['hidden']).dict()
        await db.client.expenses_tracker.category.update_one({"name": data['category']}, {"$set": {"items": document['items']}})
    
    await analytics_data()


async def delete_item(data):
    document = await db.client.expenses_tracker.category.find_one({"name": data['category']})
    if document:
        del document['items'][data['_id']]
        await db.client.expenses_tracker.category.update_one({"name": data['category']}, {"$set": {"items": document['items']}})
    
    await analytics_data()


async def analytics_data():
    categories = ["Grocery", "Food", "Entertainment", "Travelling"]
    total = []
    count = []
    for catagory in categories:
        _total = 0
        document = await db.client.expenses_tracker.category.find_one({"name": catagory})
        if document:
            for item in document['items'].values():
               _total += item['price'] if item['hidden'] is False else 0
        
        total.append(_total)
        count.append(len(document['items']) if document else 0)

    await ws_manager.broadcast_task_progress(json.dumps({"data": { "total": total, "count": count, "labels": categories}}), "analytics")

