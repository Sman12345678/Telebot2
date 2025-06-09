Info = {
    "Usage": "/gen2 [prompt]",
    "Description": "Generate an image (Flux model)."
}

import requests
from io import BytesIO

async def execute(message, bot, sender_id=None):
    prompt = message.text.partition(" ")[2].strip()
    if not prompt:
        return "❌ Please provide a prompt for image generation. Usage: <code>/gen2 your prompt</code>"

    await bot.send_message(message.chat.id, "🎨 Generating your image...")

    api_url = f"https://kaiz-apis.gleeze.com/api/flux?prompt={prompt}&apikey=2d91ea21-2c65-4edc-b601-8d06085c8358"
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            image_data = BytesIO(response.content)
            image_data.seek(0)
            await bot.send_photo(message.chat.id, photo=image_data, caption=f"🖼️ <b>Generated image for:</b> <i>{prompt}</i>", parse_mode="HTML")
            return None
        else:
            return "🚨 Failed to generate the image. Please try again later."
    except Exception as e:
        return f"🚨 An error occurred: <code>{e}</code>"

def register(dp):
    @dp.message_handler(commands=["gen2"])
    async def _cmd(message):
        await execute(message, message.bot, sender_id=message.from_user.id)
