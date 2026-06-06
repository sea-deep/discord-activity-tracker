import asyncio
from core.bot import ActivityTrackerClient
from config import TOKEN, CHANNEL_ID, LOGGING_FOR
from utils.logger import logger

async def main():
    if not TOKEN:
        logger.error("Missing TOKEN in .env file.")
        return
    if not CHANNEL_ID or not LOGGING_FOR:
        logger.error("Missing CHANNEL_ID or LOGGING_FOR in .env file.")
        return

    client = ActivityTrackerClient()
    try:
        await client.start(TOKEN)
    except asyncio.CancelledError:
        pass
    finally:
        if not client.is_closed():
            await client.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
