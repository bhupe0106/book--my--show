"""
MongoDB Connection Module for BookMyShow
"""
import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from dotenv import load_dotenv
from typing import Optional

# Load environment variables
load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
MONGODB_DATABASE = os.getenv("MONGODB_DATABASE", "bookshow")


class MongoDBConnection:
    """Singleton class for MongoDB connection"""
    
    _instance: Optional['MongoDBConnection'] = None
    _client: Optional[MongoClient] = None
    _db = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MongoDBConnection, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize MongoDB connection"""
        if self._client is None:
            self.connect()
    
    def connect(self):
        """Connect to MongoDB"""
        try:
            self._client = MongoClient(
                MONGODB_URI,
                serverSelectionTimeoutMS=5000,
                connectTimeoutMS=10000,
                retryWrites=True
            )
            
            # Verify connection
            self._client.admin.command('ping')
            self._db = self._client[MONGODB_DATABASE]
            
            print(f"✅ Connected to MongoDB at {MONGODB_URI}")
            print(f"📊 Database: {MONGODB_DATABASE}")
            
            return True
        
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            print(f"❌ Failed to connect to MongoDB: {e}")
            print(f"   Make sure MongoDB is running at {MONGODB_URI}")
            raise e
        except Exception as e:
            print(f"❌ Error connecting to MongoDB: {e}")
            raise e
    
    def get_db(self):
        """Get database instance"""
        if self._db is None:
            self.connect()
        return self._db
    
    def get_client(self):
        """Get MongoDB client instance"""
        if self._client is None:
            self.connect()
        return self._client
    
    def close(self):
        """Close MongoDB connection"""
        if self._client:
            self._client.close()
            self._client = None
            self._db = None
            print("✅ MongoDB connection closed")
    
    def is_connected(self) -> bool:
        """Check if connected to MongoDB"""
        try:
            if self._client:
                self._client.admin.command('ping')
                return True
        except:
            pass
        return False


def get_database():
    """Get MongoDB database instance"""
    connection = MongoDBConnection()
    return connection.get_db()


def close_database():
    """Close MongoDB connection"""
    connection = MongoDBConnection()
    connection.close()


# Collection names
class Collections:
    USERS = "users"
    MOVIES = "movies"
    THEATERS = "theaters"
    SHOWS = "shows"
    SEATS = "seats"
    BOOKINGS = "bookings"
    BOOKING_DETAILS = "booking_details"
    PAYMENTS = "payments"
