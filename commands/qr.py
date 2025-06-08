Info = {
    "Usage": "/qr <text or link>",
    "Description": "Generate a QR code for any link or text."
}

import qrcode
from io import BytesIO

async def execute(message, bot, sender_id=None):
    text = message.text.partition(" ")[2].strip()
    if not text:
        return "❗ Usage: <code>/qr &lt;link or text&gt;</code>"
    try:
        qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M)
        qr.add_data(text)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        output = BytesIO()
        img.save(output, format="PNG")
        output.seek(0)
        await bot.send_photo(message.chat.id, photo=output, caption=f"🟦 QR Code for:\n<code>{text}</code>", parse_mode="HTML")
        return None
    except Exception as e:
        return f"🚨 Error generating QR code: <code>{e}</code>"

def register(dp):
    @dp.message_handler(commands=["qr"])
    async def _cmd(message):
        await execute(message, message.bot, sender_id=message.from_user.id)
