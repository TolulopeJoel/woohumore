import random
import wave

import requests
from django.conf import settings
from pyht import Client
from pyht.client import TTSOptions


def create_audio(post_id, text, channels=1, sampwidth=2, framerate=24000) -> dict:
    """Creates an audio file from the given text using a text-to-speech (TTS) client."""
    file_path = f"{post_id}_output.wav"
    voice = random.choice(settings.PLAY_VOICE)

    try:
        return _create_sdk_audio(
            text, voice, file_path, channels, sampwidth, framerate
        )
    # if creating audio with SDK fails, use API instead
    except requests.exceptions.HTTPError:
        return _create_api_audio(text, voice)


def _create_sdk_audio(text, voice, file_path, channels, sampwidth, framerate):
    """Creates audio using the SDK."""
    client = Client(
        user_id=settings.PLAY_USER_ID,
        api_key=settings.PLAY_API_KEY,
    )

    options = TTSOptions(voice=voice)

    with wave.open(file_path, 'w') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(sampwidth)
        wf.setframerate(framerate)

        for chunk in client.tts(text, options):
            # convert chunk to bytes and write to the WAV file
            wf.writeframes(chunk)
        return {"path": file_path}


def _create_api_audio(text, voice):
    """Creates audio using the play.ht API as an alternative."""
    url = "https://play.ht/api/v2/tts"
    headers = {
        "AUTHORIZATION": f"Bearer {settings.PLAY_API_KEY}",
        "X-USER-ID": settings.PLAY_USER_ID,
        "accept": "text/event-stream",
        "content-type": "application/json",
    }

    data = {
        "text": text,
        "voice": voice,
        "voice_engine": "PlayHT2.0",
    }

    session = requests.Session()
    with session.post(url, headers=headers, json=data) as response:
        return response.content
