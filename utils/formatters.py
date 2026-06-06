import discord
from datetime import datetime, timezone

def get_duration_string(state_times, state_key):
    """Calculates duration since the last state change and resets the timer."""
    last_time = state_times.get(state_key)
    now = datetime.now(timezone.utc)
    state_times[state_key] = now
    
    if last_time is None:
        return ""
        
    diff = now - last_time
    seconds = int(diff.total_seconds())
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    parts = []
    if hours > 0: parts.append(f"{hours}h")
    if minutes > 0: parts.append(f"{minutes}m")
    if seconds > 0 or not parts: parts.append(f"{seconds}s")
    
    return " ".join(parts)

def get_status_emoji(status):
    status_str = str(status)
    if status_str == "online": return "🟢"
    if status_str == "idle": return "🌙"
    if status_str == "dnd": return "🔴"
    if status_str == "invisible": return "👻"
    return "⚪"

def get_activity_string(a):
    if isinstance(a, discord.CustomActivity):
        emoji = f"{a.emoji} " if getattr(a, 'emoji', None) else ""
        return f"💭 **Custom Status:** {emoji}{a.name}"
    elif isinstance(a, discord.Spotify):
        url = f"https://open.spotify.com/track/{a.track_id}" if getattr(a, 'track_id', None) else ""
        title = f"[{a.title}]({url})" if url else f"**{a.title}**"
        main_text = f"🎵 **Spotify:** {title}"
        sub_text = f"\n-# 👤 {a.artist} • 💿 {a.album}"
        return f"{main_text}{sub_text}"
    elif hasattr(a, 'type'):
        act_type = getattr(a.type, 'name', 'playing').title()
        name = a.name or "Unknown"
        
        emoji = "🎮"
        type_val = getattr(a, 'type', None)
        if type_val == discord.ActivityType.watching:
            emoji = "📺"
        elif type_val == discord.ActivityType.listening:
            emoji = "🎧"
        elif type_val == discord.ActivityType.streaming:
            emoji = "📡"
            
        url = getattr(a, 'url', None)
        title = f"[{name}]({url})" if url else f"**{name}**"
        main_text = f"{emoji} **{act_type}** {title}"
            
        extras = []
        if getattr(a, 'details', None): extras.append(f"Details: {a.details}")
        if getattr(a, 'state', None): extras.append(f"State: {a.state}")
        
        # Extremely verbose Rich Presence details
        assets = getattr(a, 'assets', None)
        if assets:
            large_text = getattr(assets, 'large_text', None)
            if large_text:
                extras.append(f"Large Image: {large_text}")
                
            small_text = getattr(assets, 'small_text', None)
            if small_text:
                extras.append(f"Small Image: {small_text}")
        
        if extras:
            return f"{main_text}\n-# {' • '.join(extras)}"
        else:
            return main_text
    else:
        return f"🔹 **{a.name}**"
