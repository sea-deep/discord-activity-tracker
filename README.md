# Discord Activity Tracker

A Python script designed to track and log a specific Discord user's presence, custom statuses, and rich presence activities using a self-bot approach. 

This project utilizes [discord.py-self](https://github.com/dolfies/discord.py-self) to authenticate as a standard user account. Since traditional Discord bots are restricted from accessing detailed user presence unless they share mutual servers (and require privileged intents), this script operates from your personal account to natively monitor presence data.

## Features
The tracker logs the following user activities:
* **Online Status**: Tracks transitions between Online, Idle, Do Not Disturb, and Offline/Invisible.
* **Custom Status**: Logs changes to the user's custom status message and associated emojis.
* **Rich Presence**: Monitors detailed activities such as games played, Spotify listening sessions (including song titles and artists), YouTube watching activity, and streaming status.
* **Duration Tracking**: Records and calculates the exact duration of each tracked activity or status.
* **Mutual Server Tracking**: Seamlessly tracks the target user via shared server presence, even if the user is not on your friends list.

---

## Requirements

* **Python 3.8+** installed on your system. 
  * [Windows Installation Guide](https://docs.python.org/3/using/windows.html)
  * [macOS Installation Guide](https://docs.python.org/3/using/mac.html)
  * [Linux Installation Guide](https://docs.python.org/3/using/unix.html)
* A Discord User Token (See the guide below).

It is highly recommended to run this project inside a Python Virtual Environment (`venv`) to prevent dependency conflicts with other projects.

---

## Getting Your Discord Token

To use this script, you must obtain your personal Discord user token. **Never share this token with anyone.**

1. Open Discord in your web browser and log in.
2. Press `Ctrl + Shift + I` (or `Cmd + Option + I` on macOS) to open the browser's Developer Tools.
3. Navigate to the **Console** tab.
4. Paste the following script into the console and press Enter:

```javascript
const iframe = document.createElement('iframe');
document.body.appendChild(iframe);
console.log('Token:', JSON.parse(iframe.contentWindow.localStorage.token));
iframe.remove();
```

5. Your token will be printed in the console. Copy the string value without the surrounding quotes.

---

## Quick Start Guide

### 1. Clone the Repository
Clone this repository to your local machine and navigate to the project directory:
```bash
git clone https://github.com/sea-deep/discord-activity-tracker.git
cd discord-activity-tracker
```

### 2. Set up a Virtual Environment
Create and activate a virtual environment:
```bash
# On Linux/macOS
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
.\venv\Scripts\activate
```

### 3. Install Dependencies
Install the required packages using `pip`:
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Rename the included `.env.example` file to `.env` and configure your credentials:
```env
# Your personal Discord User Token
TOKEN="your_discord_token_here"

# The ID of the Discord Server Channel where you want the logs to be sent
CHANNEL_ID=123456789012345678

# The Discord ID of the user you want to track
LOGGING_FOR=987654321098765432
```
*(To get IDs, go to Discord Settings -> Advanced -> Enable "Developer Mode". Right-click a user or channel and click "Copy ID")*

### 5. Run the Tracker
Start the script:
```bash
python main.py
```
If configured correctly, the bot will log into your account and begin routing presence updates to your designated channel.

---

## Disclaimer
**Use this software at your own risk.** Automating user accounts (self-botting) is against Discord's Terms of Service. While `discord.py-self` takes precautions to mimic official clients, there is always a risk of account termination if the API is abused.

## Credits
This project relies heavily on the [discord.py-self](https://github.com/dolfies/discord.py-self) wrapper.
