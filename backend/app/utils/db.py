from motor.motor_asyncio import AsyncIOMotorClient
from .config import settings
import certifi
import asyncio

class Database:
    client: AsyncIOMotorClient = None
    db = None

db = Database()

async def connect_to_mongo():
    # Adding certifi for SSL certificates on cloud providers
    # and adding a timeout for better error handling
    try:
        # For MongoDB Atlas on some cloud providers (like Railway),
        # we need to be very explicit about the SSL/TLS configuration.
        # We use tlsCAFile from certifi to ensure root certificates are found.
        db.client = AsyncIOMotorClient(
            settings.MONGODB_URL,
            tlsCAFile=certifi.where(),
            serverSelectionTimeoutMS=10000, # Increased timeout for cloud network latency
            connectTimeoutMS=10000,
            tls=True,
            retryWrites=True,
            # Some environments need to explicitly disable certificate revocation checks
            # if the cloud network blocks those requests, but we keep it safe by default.
        )
        # Verify connection
        await db.client.admin.command('ping')
        db.db = db.client[settings.DATABASE_NAME]
        print(f"Successfully connected to MongoDB at {settings.MONGODB_URL}")
    except Exception as e:
        print(f"Failed to connect to MongoDB: {str(e)}")
        # If it fails, we still set db.db to allow the app to start
        # but the lifespan indexes will likely fail too
        db.db = db.client[settings.DATABASE_NAME]
        raise e

async def close_mongo_connection():
    if db.client:
        db.client.close()
        print("MongoDB connection closed")

def get_db():
    return db.db
