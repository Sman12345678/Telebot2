Info = {
    "Usage": "/admin add [user_id] | /admin del [user_id] | /admin list",
    "Description": "Manage bot admins: add, remove, or list admin user IDs."
}

import json
import os
from config import ADMIN_IDS  # Main admins from config

ADMINS_FILE = "admins.json"

def load_admins():
    if not os.path.exists(ADMINS_FILE):
        return ADMIN_IDS[:]  # Start with config admins if no file
    with open(ADMINS_FILE, "r") as f:
        return json.load(f)

def save_admins(admins):
    with open(ADMINS_FILE, "w") as f:
        json.dump(admins, f)

def is_admin(user_id):
    admins = load_admins()
    return user_id in admins

async def execute(message, bot, sender_id=None, args=None):
    if not is_admin(sender_id):
        return "[⛔] You do not have permission to manage admins."
    
    args = (args or "").split()
    if not args:
        return (
            "Usage:\n"
            "/admin add [user_id]\n"
            "/admin del [user_id]\n"
            "/admin list"
        )
    
    action = args[0].lower()
    admins = load_admins()
    
    if action == "add" and len(args) == 2:
        try:
            new_admin = int(args[1])
        except ValueError:
            return "[!] User ID must be a number."
        if new_admin in admins:
            return f"[!] User ID [{new_admin}] is already an admin."
        admins.append(new_admin)
        save_admins(admins)
        return f"[✅] User ID [{new_admin}] added as admin."
    
    elif action == "del" and len(args) == 2:
        try:
            del_admin = int(args[1])
        except ValueError:
            return "[!] User ID must be a number."
        if del_admin not in admins:
            return f"[!] User ID [{del_admin}] is not an admin."
        if del_admin in ADMIN_IDS:
            return "[⛔] Cannot remove a main admin defined in config."
        admins.remove(del_admin)
        save_admins(admins)
        return f"[✅] User ID [{del_admin}] removed from admins."
    
    elif action == "list":
        return "[Current admins:]\n" + "\n".join(f"[{a}]" for a in admins)
    
    else:
        return (
            "[Invalid usage.]\n"
            "/admin add [user_id]\n"
            "/admin del [user_id]\n"
            "/admin list"
        )
