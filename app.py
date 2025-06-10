import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ParseMode
from aiogram.utils import executor
from dotenv import load_dotenv
from flask import Flask,render_template
from threading import Thread
import sqlite3
import pkgutil
import importlib
import commands

# Register all command callback handlers automatically
from messageHandler import handle_message, register_command_handlers

# Load env vars
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# SQLite DB: create tables if not exist
def init_db():
    with sqlite3.connect("bot_data.db") as conn:
        c = conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            chat_id INTEGER,
            sender TEXT,
            message TEXT,
            is_image INTEGER DEFAULT 0,
            is_file INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""")
        conn.commit()
init_db()


bot = Bot(token=TELEGRAM_BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

register_command_handlers(dp)

@dp.message_handler(content_types=types.ContentTypes.ANY)
async def universal_handler(message: types.Message):
    await handle_message(message, bot)

flask_app = Flask(__name__)
@flask_app.route('/')
def index():
    return render_template("index.html")

for loader, name, is_pkg in pkgutil.iter_modules(commands.__path__):
    module = importlib.import_module(f'commands.{name}')
    if hasattr(module, "oncallback"):
        # Each command must prefix its callback_data with its module name (e.g. rps_, another_command_)
        dp.register_callback_query_handler(
            getattr(module, "oncallback"),
            lambda c, n=name: c.data and c.data.startswith(f"{n}_")
        )

def run_flask():
    flask_app.run(host="0.0.0.0", port=8080, use_reloader=False)

if __name__ == "__main__":
    Thread(target=run_flask).start()
    logging.info("🚀 Telegram bot and Flask web server running!")
    executor.start_polling(dp, skip_updates=True)
