from pymongo import MongoClient

def connectDB(DB_URL:str) -> MongoClient:
    try:
        client:MongoClient = MongoClient(DB_URL)
        return client if client else print("Failed to connect to MongoDB")
    except Exception as e:
        print(e)
        return
