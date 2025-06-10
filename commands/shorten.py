Info = {
    "Usage": "/shorten [url]",
    "Description": "Shorten a link using TinyURL."
}

import requests

async def execute(message, bot, sender_id=None):
    url = message.text.partition(" ")[2].strip()
    if not url:
        await bot.send_message(message.chat.id, "[!] Usage: /shorten [url]")
        return
    try:
        api_url = f"https://tinyurl.com/api-create.php?url={url}"
        resp = requests.get(api_url, timeout=10)
        if resp.status_code == 200 and resp.text.startswith("http"):
            await bot.send_message(message.chat.id, f"[🔗 Shortened URL:]\n{resp.text}")
        else:
            await bot.send_message(message.chat.id, "[❌] Could not shorten the link.")
    except Exception as e:
        await bot.send_message(message.chat.id, f"[❌] Error: [{e}]")
