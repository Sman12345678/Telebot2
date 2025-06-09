Info = {
    "Usage": "/help",
    "Description": "Show this help message with available commands."
}

import os
import importlib.util

async def execute(message, bot, sender_id=None):
    commands_dir = os.path.dirname(__file__)
    help_lines = [
        "╔════════════════════════════╗",
        "     🤖 KORA AI COMMANDS     ",
        "╚════════════════════════════╝",
        "",
        "Here are the available commands:",
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
                usage = info.get('Usage', f"/{cmd_name}") if info else f"/{cmd_name}"
                desc = info.get('Description', 'No description.') if info else "No description."
                help_lines.append(f"• {usage}\n    ↳ {desc}")
            except Exception as e:
                help_lines.append(f"• /{cmd_name}\n    ↳ Could not load ({e})")
    help_lines.append("")
    help_lines.append("Tip: Type /help anytime for this menu!")
    return "\n".join(help_lines)

def register(dp):
    @dp.message_handler(commands=["help"])
    async def _cmd(message):
        await message.reply(await execute(message, None, sender_id=message.from_user.id))
