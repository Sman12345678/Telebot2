Info = {
    "Usage": "/help",
    "Description": "Show this help message with available commands."
}

import os
import importlib.util

async def execute(message, bot, sender_id=None):
    commands_dir = os.path.dirname(__file__)
    help_lines = [
        "<b>🤖 <u>Welcome to KORA AI</u>!</b>",
        "Here are the available commands:",
        "<b>─────────────────────────────</b>",
        "🟢 <i>Usage:</i> <code>/command [arguments]</code>",
        "🟠 <i>Admin-only commands are marked with</i> <b>🔒</b>",
        "<b>─────────────────────────────</b>",
        "",
    ]
    for filename in sorted(os.listdir(commands_dir)):
        if filename.endswith(".py") and filename not in ("__init__.py", "help.py"):
            cmd_name = filename[:-3]
            try:
                spec = importlib.util.spec_from_file_location(cmd_name, os.path.join(commands_dir, filename))
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)
                info = getattr(mod, "Info", None)
                admin_tag = "🔒 " if info and "admin" in info.get("Description", "").lower() else ""
                if info:
                    help_lines.append(
                        f"• {admin_tag}<b>{info.get('Usage','/'+cmd_name)}</b>\n"
                        f"    <i>{info.get('Description','No description.')}</i>"
                    )
                else:
                    help_lines.append(f"• <b>/{cmd_name}</b>\n    <i>No description.</i>")
            except Exception as e:
                help_lines.append(f"• <b>/{cmd_name}</b>\n    <i>Error loading: {e}</i>")
    help_lines.append("\n<b>💡 Tip:</b> Use <code>/help</code> anytime to see this menu!")
    return "\n".join(help_lines)

def register(dp):
    @dp.message_handler(commands=["help"])
    async def _cmd(message):
        await message.reply(await execute(message, None, sender_id=message.from_user.id), parse_mode="HTML")
