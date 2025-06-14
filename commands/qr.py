Info = {
    "Usage": "/qr [Text or link]",
    "Description": "Generate a QR code for any link or text."
}

import qrcode
from io import BytesIO

async def execute(message, bot, sender_id=None):
    text = message.text.partition(" ")[2].strip()
    if not text:
        await bot.send_message(message.chat.id, "❗ Usage: /qr [link or text]")
        return

    try:
        qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M)
        qr.add_data(text)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        output = BytesIO()
        img.save(output, format="PNG")
        output.seek(0)

        await bot.send_photo(
            message.chat.id,
            photo=output,
            caption=f"🟦 QR Code for:\n<code>{text}</code>",
            parse_mode="HTML"
        )
    except Exception as e:
        await bot.send_message(
            message.chat.id,
            f"🚨 Error generating QR code: <code>{e}</code>",
            parse_mode="HTML"
        )

def register(dp):
    @dp.message_handler(commands=["qr"])
    async def _cmd(message):
        await execute(message, message.bot, sender_id=message.from_user.id)
