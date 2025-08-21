import os

from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = os.getenv("MONGO_URL", "")
DB_NAME = "inkpos_db"

client = AsyncIOMotorClient(MONGO_URL)
db = client[DB_NAME]

async def get_users_collection():
    return db.pos_users

async def get_products_collection():
    return db.products

async def get_sales_collection():
    return db.sales

async def get_enquiries_collection():
    return db.enquiries

async def get_appointments_collection():
    return db.appointments

async def get_transactions_collection():
    return db.transactions

async def get_expenses_collection():
    return db.expenses
