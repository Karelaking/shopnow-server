import logging

from pymongo import MongoClient
from pymongo.errors import (ConnectionFailure,
                            ConfigurationError,
                            ServerSelectionTimeoutError)


def connectDB(DB_URL: str, timeout: int = 5000) -> MongoClient:
	"""
    Connect to MongoDB with error handling and connection verification.
    Args:
        DB_URL (str): MongoDB connection string
        timeout (int): Connection timeout in milliseconds
        
    Returns:
        MongoClient: MongoDB client if connection successful, None otherwise
    """
	try:
		# Initialize connection with a timeout
		client = MongoClient(DB_URL, serverSelectionTimeoutMS=timeout)
		
		# Verify connection by executing a command
		client.admin.command('ping')
		
		logging.info("Successfully connected to MongoDB")
		return client
	
	except ConnectionFailure as e:
		logging.error(f"MongoDB Connection Failed: {e}")
		return None
	except ConfigurationError as e:
		logging.error(f"MongoDB Configuration Error: {e}")
		return None
	except ServerSelectionTimeoutError as e:
		logging.error(f"MongoDB Server Selection Timeout: {e}")
		return None
	except Exception as e:
		logging.error(f"Unexpected error when connecting to MongoDB: {e}")
		return None
