import random
import wave

from django.conf import settings
from pyht import Client
from pyht.client import TTSOptions
import requests


def create_audio(post_id, text, channels=1, sampwidth=2, framerate=24000) -> dict:
    """
    Creates an audio file from the given text using a text-to-speech (TTS) client.

    Uses the specified `post_id` to generate a unique audio file path.
    Randomly selects a voice from the available options.
    Sets the TTS options with the chosen voice.

    Args:
        post_id: The ID of the post.
        text: The text (post body) to convert to audio.

    Returns:
        dict: contains audio info (e.g path, url, duration).
    """
    audio_file_path = f"{post_id}_output.wav"
    talker_voice = random.choice(settings.PLAY_VOICE)

    try:
        client = Client(
            user_id=settings.PLAY_USER_ID,
            api_key=settings.PLAY_API_KEY,
        )

        options = TTSOptions(voice=talker_voice)

        with wave.open(audio_file_path, 'w') as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(sampwidth)
            wf.setframerate(framerate)

            for chunk in client.tts(text, options):
                # convert chunk to bytes and write to the WAV file
                wf.writeframes(chunk)
            return {"path": audio_file_path}

    # if creating audio with SDK fails, use play.ht API instead
    except requests.exceptions.HTTPError:
        url = "https://play.ht/api/v2/tts"
        headers = {
            "AUTHORIZATION": f"Bearer {settings.PLAY_API_KEY}",
            "X-USER-ID": settings.PLAY_USER_ID,
            "accept": "text/event-stream",
            "content-type": "application/json",
        }

        data = {
            "text": text,
            "voice": talker_voice,
            "voice_engine": "PlayHT2.0",
        }

        with requests.post(url, headers=headers, json=data) as response:
            return response.content
