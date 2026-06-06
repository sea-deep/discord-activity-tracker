import discord
import asyncio
from datetime import datetime, timezone
from utils import logger, get_duration_string, get_status_emoji, get_activity_string
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
        desktop = str(getattr(after, 'desktop_status', 'offline'))
        mobile = str(getattr(after, 'mobile_status', 'offline'))
        web = str(getattr(after, 'web_status', 'offline'))
        
        detailed_status = f"{a_status_str} (💻 {desktop} | 📱 {mobile} | 🌐 {web})"

        # 1. Deduplicated Status Tracking
        if self.current_status != detailed_status:
            # First time running, don't spam a duration for initialization
            if self.current_status is not None:
                duration_str = get_duration_string(self.state_times, "status")
                prev_main_status = self.current_status.split()[0]
                e_before = get_status_emoji(prev_main_status)
                e_after = get_status_emoji(a_status_str)
                
                log_msg = (
                    f"### 🔄 Status Update\n"
                    f"{e_before} **{prev_main_status.title()}** ➡️ {e_after} **{a_status_str.title()}**\n"
                    f"-# 💻 {desktop} | 📱 {mobile} | 🌐 {web}"
                )
                if duration_str:
                    log_msg += f"  •  ⏱️ {duration_str}"
                    
                logs.append(log_msg)
            else:
                self.state_times["status"] = datetime.now(timezone.utc)
            self.current_status = detailed_status
            
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
                    diff_logs.append(f"- 🟢 **Started:** {act}")
                for act in removed:
                    diff_logs.append(f"- 🔴 **Stopped:** {act}")
                    
                header = "### 🎮 Activity Update"
                if duration_str:
                    header += f"\n-# ⏱️ Time since last change: {duration_str}"
                    
                logs.append(header + "\n" + "\n".join(diff_logs))
            else:
                self.state_times["activity"] = datetime.now(timezone.utc)
                
            self.current_activities = a_set

        for msg in logs:
            await self.log_to_channel(msg)
