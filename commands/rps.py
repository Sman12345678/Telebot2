Info = {
    "Usage": "/rps",
    "Description": "Play continuous Rock Paper Scissors with the bot! Use the inline buttons to make your move."
}

from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import random

choices = ['rock', 'paper', 'scissors']
emojis = {'rock': '🪨', 'paper': '📄', 'scissors': '✂️'}

def determine_winner(user, bot):
    if user == bot:
        return "It's a draw!"
    wins = {
        ('rock', 'scissors'),
        ('scissors', 'paper'),
        ('paper', 'rock')
    }
    if (user, bot) in wins:
        return "You win! 🎉"
    else:
        return "You lose! 😢"

def get_rps_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=3)
    for c in choices:
        keyboard.insert(InlineKeyboardButton(
            text=f"{emojis[c]} {c.title()}", callback_data=f"rps_{c}"
        ))
    return keyboard

async def execute(message: types.Message, bot, sender_id=None):
    text = (
        "Let's play Rock Paper Scissors!\n"
        "Choose your move by pressing one of the buttons below:"
    )
    await message.reply(text, reply_markup=get_rps_keyboard())

# ----------- MODIFIED HANDLER ------------
async def oncallback(callback_query: types.CallbackQuery):
    bot = callback_query.bot
    if not callback_query.data.startswith("rps_"):
        await callback_query.answer("Invalid move.", show_alert=True)
        return

    user_choice = callback_query.data.replace("rps_", "")
    if user_choice not in choices:
        await callback_query.answer("Invalid move.", show_alert=True)
        return

    bot_choice = random.choice(choices)
    result = determine_winner(user_choice, bot_choice)
    reply = (
        f"You chose: {emojis[user_choice]} {user_choice}\n"
        f"Bot chose: {emojis[bot_choice]} {bot_choice}\n\n"
        f"{result}\n\n"
        "Play again:"
    )
    await callback_query.message.edit_text(reply, reply_markup=get_rps_keyboard())
    await callback_query.answer("Move received!")
