import os
from config import ADMIN_IDS

async def execute(message, bot, sender_id=None):
    if sender_id not in ADMIN_IDS:
        return "🚫 Only admins can use this command."
    text = message.text.partition(" ")[2]
    if not text or ".py" not in text or "\\n" not in text:
        return "❌ Invalid format. Usage: /install filename.py\\n<code>"
    filename, code = text.split("\\n", 1)
    filename = filename.strip()
    if not filename.endswith(".py") or "/" in filename or "\\" in filename:
        return "❌ Invalid filename."
    file_path = os.path.join("commands", filename)
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(code.strip())
        return f"✅ commands/{filename} installed successfully."
    except Exception as e:
        return f"🚨 Error installing file: <code>{e}</code>"

def register(dp):
    @dp.message_handler(commands=["install"])
    async def _cmd(message):
        await message.reply(await execute(message, None, sender_id=message.from_user.id), parse_mode="HTML")
