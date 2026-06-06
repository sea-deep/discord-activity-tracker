import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

TOKEN = os.getenv("TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID", 0))
LOGGING_FOR = int(os.getenv("LOGGING_FOR", 0))
