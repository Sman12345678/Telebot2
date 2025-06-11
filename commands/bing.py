Info = {
    "Usage": "/bing [your prompt]",
    "Description": "Generate images using Bing Image Creator API."
}

import requests
from io import BytesIO

API_BASE = "https://bing-image-creator-l1if.onrender.com"
API_URL = f"{API_BASE}/api/gen"
API_KEY = "sman-apiA1B2C3D4E5"

async def execute(message, bot, sender_id=None):
    prompt = message.text.partition(" ")[2].strip()
    if not prompt:
        await bot.send_message(message.chat.id, "❗ Usage: /bing [your prompt]")
        return

    msg = await bot.send_message(message.chat.id, "🖼️ Generating Bing images...")

    params = {
        "prompt": prompt,
        "api_key": API_KEY
    }
    try:
        response = requests.get(API_URL, params=params, timeout=90)
        if response.status_code == 200:
            data = response.json()
            if not data or not isinstance(data, list) or not data[0].get("url"):
                await bot.send_message(message.chat.id, "❌ No images returned by API.")
                return

            # Compose full image URLs
            full_urls = [API_BASE + item["url"] for item in data if "url" in item]

            sent = False
            for i, url in enumerate(full_urls):
                img_resp = requests.get(url, timeout=60)
                if img_resp.status_code == 200:
                    img_bytes = BytesIO(img_resp.content)
                    img_bytes.name = f"bing_{i+1}.jpg"
                    await bot.send_photo(
                        message.chat.id,
                        photo=img_bytes,
                        caption=f"🖼️ <b>Bing Image {i+1}</b>\nPrompt: <i>{prompt}</i>",
                        parse_mode="HTML"
                    )
                    sent = True
                else:
                    await bot.send_message(message.chat.id, f"🚨 Failed to download image {i+1}.")
            if not sent:
                await bot.send_message(message.chat.id, "❌ Could not send any images.")
        else:
            await bot.send_message(message.chat.id, f"🚨 Failed to generate images. API code {response.status_code}.")
    except Exception as e:
        await bot.send_message(message.chat.id, f"🚨 An error occurred: <code>{e}</code>", parse_mode="HTML")
    finally:
        try:
            await msg.delete()
        except Exception:
            pass

def register(dp):
    @dp.message_handler(commands=["bing"])
    async def _cmd(message):
        await execute(message, message.bot, sender_id=message.from_user.id)
