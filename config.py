import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

TOKEN = os.getenv("TOKEN")

_channel_id = os.getenv("CHANNEL_ID")
CHANNEL_ID = int(_channel_id) if _channel_id and _channel_id.isdigit() else 0

_logging_for = os.getenv("LOGGING_FOR")
LOGGING_FOR = int(_logging_for) if _logging_for and _logging_for.isdigit() else 0
