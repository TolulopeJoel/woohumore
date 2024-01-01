from pyht import Client
from pyht.client import TTSOptions
import wave
from django.conf import settings

client = Client(
    user_id=settings.PLAY_USER_ID,
    api_key=settings.PLAY_API_KEY,

)
options = TTSOptions(
    voice="s3://voice-cloning-zero-shot/801a663f-efd0-4254-98d0-5c175514c3e8/jennifer/manifest.json",
)


def create_audio(text):
    with wave.open("output.wav", 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(24000)

        for chunk in client.tts(text, options):
            # Convert the chunk to bytes and write to the WAV file
            wf.writeframes(chunk)
