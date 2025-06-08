import os
from config import ADMIN_IDS

async def execute(message, bot, sender_id=None):
    if sender_id not in ADMIN_IDS:
        return "🚫 Only admins can use this command."
    filename = message.text.partition(" ")[2].strip()
    if not filename:
        return "❗ Usage: <code>/file filename_or_path</code>"
    if ".." in filename or filename.startswith("/") or "\\" in filename:
        return "❌ Invalid filename or path."
    file_path = os.path.join(os.getcwd(), filename)
    if not os.path.isfile(file_path):
        return f"❌ File <b>{filename}</b> does not exist."
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            code = f.read()
        if len(code) > 3500:
            code = code[:3500] + "\n... (truncated)"
        return f"<b>📄 {filename} code:</b>\n<pre>{code}</pre>"
    except Exception as e:
        return f"🚨 Error reading file: <code>{e}</code>"

def register(dp):
    @dp.message_handler(commands=["file"])
    async def _cmd(message):
        await message.reply(await execute(message, None, sender_id=message.from_user.id), parse_mode="HTML")
