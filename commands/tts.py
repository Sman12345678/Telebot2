Info = {
    "Usage": "/tts [your text here]",
    "Description": "Convert text to speech and send as audio."
}

from gtts import gTTS
from io import BytesIO

async def execute(message, bot, sender_id=None):
    text = message.text.partition(" ")[2].strip()
    if not text:
        await bot.send_message(message.chat.id, "[!] Usage: /tts [your text here]")
        return

    try:
        # Generate speech using gTTS and save to BytesIO
        tts = gTTS(text=text, lang="en")
        audio_bytes = BytesIO()
        tts.write_to_fp(audio_bytes)
        audio_bytes.seek(0)
        audio_bytes.name = "speech.mp3"
        await bot.send_audio(message.chat.id, audio=audio_bytes, title="TTS")
    except Exception as e:
        await bot.send_message(message.chat.id, f"[❌] Error generating speech: [{e}]")
