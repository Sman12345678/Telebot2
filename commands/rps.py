Info = {
    "Usage": "/rps [rock|paper|scissors]",
    "Description": "Play Rock Paper Scissors with the bot."
}

from aiogram import types
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

async def execute(message: types.Message, bot, sender_id=None):
    user_choice = message.text.partition(" ")[2].strip().lower()
    if user_choice not in choices:
        await message.reply("[!] Usage: /rps [rock|paper|scissors]")
        return
    bot_choice = random.choice(choices)
    result = determine_winner(user_choice, bot_choice)
    reply = (
        f"You chose: {emojis[user_choice]} {user_choice}\n"
        f"Bot chose: {emojis[bot_choice]} {bot_choice}\n\n"
        f"{result}"
    )
    await message.reply(reply)
