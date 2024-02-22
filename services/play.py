import requests
from django.conf import settings


class PlayAudioService:
    def __init__(self):
        self.headers = {
            "AUTHORIZATION": f"Bearer {settings.PLAY_API_KEY}",
            "X-USER-ID": settings.PLAY_USER_ID,
            "accept": "text/event-stream",
            "content-type": "application/json",
        }
        self.session = requests.Session()
        self.audio_length = 0

    def create_audio(self, text: str, voice: str):
        url = "https://play.ht/api/v2/tts"

        payload = {"text": text, "voice": voice, "voice_engine": "PlayHT2.0"}

        response = self.session.post(url, headers=self.headers, json=payload)
        if response.status_code == 200:
            rp_data = response.json()

            # set duration length
            self.audio_length = rp_data["duration"]

            return rp_data["url"]
