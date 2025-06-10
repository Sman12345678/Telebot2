Info = {
    "Usage": "/tts [your text here]",
    "Description": "Convert text to speech and send as audio."
}

import pyttsx3
import tempfile
import os
from io import BytesIO

async def execute(message, bot, sender_id=None, args=None):
    text = args or ""
    if not text.strip():
        return "[!] Please provide the text to convert to speech. Usage: /tts [your text here]"
    
    # Generate speech and save to a temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
        filename = tmp_file.name
    try:
        engine = pyttsx3.init()
        engine.save_to_file(text, filename)
        engine.runAndWait()
        # Read file content into memory and send as audio
        with open(filename, "rb") as audio:
            audio_bytes = BytesIO(audio.read())
            audio_bytes.name = "speech.mp3"
            await bot.send_audio(message.chat.id, audio=audio_bytes, title="TTS")
        return None  # Reply is the audio
    except Exception as e:
        return f"[❌] Error generating speech: [{e}]"
    finally:
        if os.path.exists(filename):
            os.remove(filename)
