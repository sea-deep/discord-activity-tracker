# Simple Discord User Activity Tracker

This is a lightweight script using `discord.py-self` to track the activity of a single specific user and log their actions directly to a designated Discord channel.

## Features
- **Presence Updates:** Logs when the target user changes status (Online/Offline) or activity (playing a game).
- **Voice Updates:** Logs when the target user joins, leaves, or moves voice channels, as well as mute/deafen states.
- **Message Tracking:** Logs when the user sends a message.

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Configure `.env`:
   ```env
   TOKEN=your_user_token_here
   CHANNEL_ID=000000000000000000
   LOGGING_FOR=000000000000000000
   ```
   - `TOKEN`: The Discord account running the script.
   - `CHANNEL_ID`: The channel where the bot will send the logs.
   - `LOGGING_FOR`: The user ID of the person you are tracking.

3. Run the tracker:
   ```bash
   python main.py
   ```
