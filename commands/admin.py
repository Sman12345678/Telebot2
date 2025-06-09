Info = {
    "Usage": "/admin add [user_id] | /admin del [user_id] | /admin list",
    "Description": "Manage bot admins: add, remove, or list admin user IDs."
}

from config import ADMIN_IDS  # Example: ADMIN_IDS = [123456]
extra_admins = []  # Temporary session-only admins

def is_admin(user_id):
    return user_id in ADMIN_IDS or user_id in extra_admins

async def execute(message, bot, sender_id=None, args=None):
    if not is_admin(sender_id):
        await bot.send_message(message.chat.id, "[⛔] You do not have permission to manage admins.")
        return

    if args is None:
        args = message.text.partition(" ")[2].strip()
    args = args.split()

    if not args:
        await bot.send_message(message.chat.id,
            "Usage:\n"
            "/admin add [user_id]\n"
            "/admin del [user_id]\n"
            "/admin list"
        )
        return

    action = args[0].lower()

    if action == "add" and len(args) == 2:
        try:
            new_admin = int(args[1])
        except ValueError:
            await bot.send_message(message.chat.id, "[!] User ID must be a number.")
            return
        if new_admin in ADMIN_IDS or new_admin in extra_admins:
            await bot.send_message(message.chat.id, f"[!] User ID [{new_admin}] is already an admin.")
            return
        extra_admins.append(new_admin)
        await bot.send_message(message.chat.id, f"[✅] User ID [{new_admin}] added as admin.")

    elif action == "del" and len(args) == 2:
        try:
            del_admin = int(args[1])
        except ValueError:
            await bot.send_message(message.chat.id, "[!] User ID must be a number.")
            return
        if del_admin in ADMIN_IDS:
            await bot.send_message(message.chat.id, "[⛔] Cannot remove a main admin defined in config.")
            return
        if del_admin not in extra_admins:
            await bot.send_message(message.chat.id, f"[!] User ID [{del_admin}] is not an extra admin.")
            return
        extra_admins.remove(del_admin)
        await bot.send_message(message.chat.id, f"[✅] User ID [{del_admin}] removed from admins.")

    elif action == "list":
        full_admins = ADMIN_IDS + extra_admins
        await bot.send_message(
            message.chat.id,
            "[Current admins:]\n" + "\n".join(f"[{a}]" for a in full_admins)
        )
    else:
        await bot.send_message(message.chat.id,
            "[Invalid usage.]\n"
            "/admin add [user_id]\n"
            "/admin del [user_id]\n"
            "/admin list"
        )

def register(dp):
    @dp.message_handler(commands=["admin"])
    async def _cmd(message):
        await execute(message, message.bot, sender_id=message.from_user.id)
