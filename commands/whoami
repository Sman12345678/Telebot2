Info = {
    "Usage": "/whoami",
    "Description": "Show your Telegram user info."
}

async def execute(message, bot, sender_id=None):
    user = message.from_user
    user_id = user.id
    username = f"@{user.username}" if user.username else "[no username]"
    mention = f"[{user.first_name}](tg://user?id={user.id})"
    first_name = user.first_name
    text = (
        f"[👤 Your Telegram info:]\n"
        f"[ID:] {user_id}\n"
        f"[Username:] {username}\n"
        f"[Name:] {first_name}\n"
        f"[Mention:] {mention}"
    )
    await bot.send_message(message.chat.id, text, parse_mode="Markdown")
