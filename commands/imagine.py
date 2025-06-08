Info = {
    "Usage": "/imagine <prompt>",
    "Description": "Generate image and text using Kaizenji API."
}

import requests
from io import BytesIO

async def execute(message, bot, sender_id=None):
    prompt = message.text.partition(" ")[2].strip()
    if not prompt:
        return "Usage: <code>/imagine &lt;prompt&gt;</code>"
    api_url = "https://kaiz-apis.gleeze.com/api/gpt-4o-pro"
    params = {
        "ask": prompt,
        "uid": "sman",
        "imageUrl": "",
        "apikey": "2d91ea21-2c65-4edc-b601-8d06085c8358"
    }
    try:
        resp = requests.get(api_url, params=params, timeout=30)
        if resp.status_code != 200:
            return f"❌ API error: {resp.status_code}"
        data = resp.json()
        image_url = data.get("images")
        text_response = data.get("response", "")
        if image_url:
            img_response = requests.get(image_url, stream=True, timeout=30)
            if img_response.status_code == 200:
                image_bytes = BytesIO(img_response.content)
                await bot.send_photo(message.chat.id, photo=image_bytes, caption="🖼️ <b>Generated Image</b>", parse_mode="HTML")
            else:
                await bot.send_message(message.chat.id, "❌ Failed to fetch the generated image.")
        if text_response:
            return text_response
        return None
    except Exception as e:
        return f"🚨 Error: <code>{e}</code>"

def register(dp):
    @dp.message_handler(commands=["imagine"])
    async def _cmd(message):
        await message.reply(await execute(message, message.bot, sender_id=message.from_user.id), parse_mode="HTML")
