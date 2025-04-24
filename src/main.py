import sys
from os import getenv

from dotenv import load_dotenv
from uvicorn import run

from app import app
from database.connetDB import connectDB  # Note: There's a typo in import path "connetDB"

# Load environment variables first
load_dotenv()

# Get environment variables with proper fallbacks
DB_URL = getenv('DB_URL')
# Fix the bitwise OR operator (|) - should be logical OR
PORT = int(getenv('PORT', 8000))


# Main entry point of the application
def main():
	# Check if DB_URL exists
	if not DB_URL:
		print("Error: DB_URL environment variable not set")
		sys.exit(1)
	
	try:
		# Pass the actual DB_URL to connectDB
		client = connectDB(DB_URL)
		
		if client:
			print("Connected to MongoDB")
		else:
			print("Failed to connect to MongoDB")
			sys.exit(1)
	except Exception as e:
		print(f"Error: {e}")
		sys.exit(1)
	
	# Run the application
	run(app, host="0.0.0.0", port=PORT)


if __name__ == '__main__':
	main()
