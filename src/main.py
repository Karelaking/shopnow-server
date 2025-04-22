from app import app
from os import getenv
from uvicorn import run
from dotenv import load_dotenv
from database.connetDB import connectDB

load_dotenv()

DB_URL:str = getenv('DB_URL')
PORT:int = int(getenv('PORT')) | 8000

# main entry point
def main():
    try:
        client = connectDB(DB_URL)
        print("Connected to MongoDB") if client else print("Failed to connect to MongoDB")
    except Exception as e:
        print(e)
        return
    run(app, host="0.0.0.0", port=PORT)



if __name__ == '__main__':
    main()
