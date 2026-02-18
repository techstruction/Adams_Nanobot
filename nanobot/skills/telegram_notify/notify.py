import asyncio
import sys
import json
from pathlib import Path
from telegram import Bot

async def send_notification(chat_id: str, text: str):
    config_path = Path.home() / ".nanobot" / "config.json"
    if not config_path.exists():
        print("Error: config.json not found")
        return
    
    try:
        with open(config_path, "r") as f:
            config = json.load(f)
        
        token = config.get("channels", {}).get("telegram", {}).get("token")
        if not token:
            print("Error: Telegram token not found in config.json")
            return
        
        async with Bot(token) as bot:
            await bot.send_message(chat_id=chat_id, text=text, parse_mode='HTML')
            print(f"Successfully sent message to {chat_id}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 notify.py <chat_id> <message>")
        sys.exit(1)
    
    asyncio.run(send_notification(sys.argv[1], sys.argv[2]))
