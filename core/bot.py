import discord
import asyncio
from datetime import datetime, timezone
from utils.logger import logger
from utils.formatters import get_duration_string, get_status_emoji, get_activity_string
from config import CHANNEL_ID, LOGGING_FOR

class ActivityTrackerClient(discord.Client):
    def __init__(self):
        super().__init__()
        
        self.state_times = {
            "status": None,
            "activity": None
        }
        
        # Track the last known state to prevent duplicate logs from multiple mutual guilds
        self.current_status = None
        self.current_activities = set()

    async def keep_alive_subscription(self):
        """Discord gateway drops subscriptions after a few minutes. This keeps it alive."""
        await self.wait_until_ready()
        while not self.is_closed():
            try:
                profile = await self.fetch_user_profile(LOGGING_FOR)
                if profile.mutual_guilds:
                    for mut_guild in profile.mutual_guilds:
                        guild_obj = self.get_guild(mut_guild.id)
                        if guild_obj:
                            await guild_obj.subscribe_to(members=[discord.Object(id=LOGGING_FOR)])
            except Exception:
                pass
            await asyncio.sleep(60)  # Renew every 60 seconds

    async def setup_hook(self):
        # Start the background task to keep the subscription alive
        self.loop.create_task(self.keep_alive_subscription())

    async def on_ready(self):
        logger.info(f"Logged in as {self.user} (ID: {self.user.id})")
        logger.info(f"Tracking user ID: {LOGGING_FOR}")
        logger.info(f"Logging to channel ID: {CHANNEL_ID}")
        logger.info("Keep-alive subscription task started.")

    async def log_to_channel(self, message: str):
        channel = self.get_channel(CHANNEL_ID)
        if channel:
            try:
                await channel.send(message)
            except Exception as e:
                logger.error(f"Failed to send log message: {e}")
        else:
            logger.warning(f"Could not find channel with ID {CHANNEL_ID}")

    async def on_presence_update(self, before, after):
        # In discord.py-self, 'after' can be a Member or a Relationship (friend)
        user_id = getattr(after, 'id', getattr(getattr(after, 'user', None), 'id', None))
        if user_id != LOGGING_FOR:
            return

        logs = []
        
        a_status_str = str(after.status)

        # 1. Deduplicated Status Tracking
        if self.current_status != a_status_str:
            # First time running, don't spam a duration for initialization
            if self.current_status is not None:
                duration_str = get_duration_string(self.state_times, "status")
                e_before = get_status_emoji(self.current_status)
                e_after = get_status_emoji(a_status_str)
                logs.append(f"**Status:** {e_before} `{self.current_status}` ➡️ {e_after} `{a_status_str}`{duration_str}")
            else:
                self.state_times["status"] = datetime.now(timezone.utc)
            self.current_status = a_status_str
            
        # 2. Deduplicated Activity Diff Tracking
        a_act_strs = []
        if after.activities:
            a_act_strs = [get_activity_string(a) for a in after.activities]
            
        a_act_strs = list(dict.fromkeys(a_act_strs))
        a_set = set(a_act_strs)
        
        if self.current_activities != a_set:
            if self.current_activities: # Don't log "Started" for everything on first boot
                added = a_set - self.current_activities
                removed = self.current_activities - a_set
                
                duration_str = get_duration_string(self.state_times, "activity")
                diff_logs = []
                for act in added:
                    diff_logs.append(f"> 🟢 **Started:** {act}")
                for act in removed:
                    diff_logs.append(f"> 🔴 **Stopped:** {act}")
                    
                logs.append(f"**Activity Update**{duration_str}\n" + "\n".join(diff_logs))
            else:
                self.state_times["activity"] = datetime.now(timezone.utc)
                
            self.current_activities = a_set

        for msg in logs:
            await self.log_to_channel(msg)
