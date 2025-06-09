Info = {
    "Usage": "/gen [prompt]",
    "Description": "Generate an image (Stable Diffusion 3.5)."
}

import requests
from io import BytesIO

async def execute(message, bot, sender_id=None):
    prompt = message.text.partition(" ")[2].strip()
    if not prompt:
        await bot.send_message(message.chat.id, "Please provide a prompt e.g. /gen cat")
        return

    await bot.send_message(message.chat.id, "🎨 Generating your image...")

    api_url = f"https://kaiz-apis.gleeze.com/api/stable-diffusion-3.5-rev2?prompt={prompt}&apikey=2d91ea21-2c65-4edc-b601-8d06085c8358"
    
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            image_data = BytesIO(response.content)
            image_data.seek(0)
            await bot.send_photo(
                message.chat.id,
                photo=image_data,
                caption=f"🖼️ <b>Generated image for:</b> <i>{prompt}</i>",
                parse_mode="HTML"
            )
        else:
            await bot.send_message(message.chat.id, "🚨 Failed to generate the image. Please try again later.")
    except Exception as e:
        await bot.send_message(message.chat.id, f"🚨 An error occurred: <code>{e}</code>", parse_mode="HTML")

def register(dp):
    @dp.message_handler(commands=["gen"])
    async def _cmd(message):
        await execute(message, message.bot, sender_id=message.from_user.id)
