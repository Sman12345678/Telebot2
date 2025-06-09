Info = {
    "Usage": "/admin add,[user_id] | /admin del,[user_id] | /admin list",
    "Description": "Manage bot admins: add, remove, or list admin user IDs."
}

from config import ADMIN_IDS  # Example: ADMIN_IDS = [123456]

extra_admins = []  # Temporary in-memory admins list

def is_admin(user_id):
    return user_id in ADMIN_IDS or user_id in extra_admins

async def execute(message, bot, sender_id=None, args=None):
    if not is_admin(sender_id):
        await bot.send_message(message.chat.id, "[⛔] You do not have permission to manage admins.")
        return

    # Extract the full text after /admin command
    full_args = message.text.partition(" ")[2].strip()

    if not full_args:
        await bot.send_message(message.chat.id,
            "Usage:\n"
            "/admin add,[user_id]\n"
            "/admin del,[user_id]\n"
            "/admin list"
        )
        return

    # Split by comma: first part = action, second part = user_id or empty
    parts = [p.strip() for p in full_args.split(",", 1)]
    action = parts[0].lower()

    if action == "list":
        full_admins = ADMIN_IDS + extra_admins
        await bot.send_message(
            message.chat.id,
            "[Current admins:]\n" + "\n".join(f"[{a}]" for a in full_admins)
        )
        return

    if len(parts) < 2:
        await bot.send_message(message.chat.id,
            "❗ Missing user ID.\nUsage:\n"
            "/admin add,[user_id]\n"
            "/admin del,[user_id]"
        )
        return

    user_id_str = parts[1]
    try:
        user_id = int(user_id_str)
    except ValueError:
        await bot.send_message(message.chat.id, "[!] User ID must be a number.")
        return

    if action == "add":
        if user_id in ADMIN_IDS or user_id in extra_admins:
            await bot.send_message(message.chat.id, f"[!] User ID [{user_id}] is already an admin.")
            return
        extra_admins.append(user_id)
        await bot.send_message(message.chat.id, f"[✅] User ID [{user_id}] added as admin.")
    elif action == "del":
        if user_id in ADMIN_IDS:
            await bot.send_message(message.chat.id, "[⛔] Cannot remove a main admin defined in config.")
            return
        if user_id not in extra_admins:
            await bot.send_message(message.chat.id, f"[!] User ID [{user_id}] is not an extra admin.")
            return
        extra_admins.remove(user_id)
        await bot.send_message(message.chat.id, f"[✅] User ID [{user_id}] removed from admins.")
    else:
        await bot.send_message(message.chat.id,
            "Invalid action.\nUsage:\n"
            "/admin add,[user_id]\n"
            "/admin del,[user_id]\n"
            "/admin list"
        )

def register(dp):
    @dp.message_handler(commands=["admin"])
    async def _cmd(message):
        await execute(message, message.bot, sender_id=message.from_user.id)
