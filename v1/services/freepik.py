import urllib.parse

import requests
from django.conf import settings


class FreePikService:
    def __init__(self):
        self.headers = {
            "Accept-Language": "en-US",
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-Freepik-API-Key": settings.FREEPIK_API_KEY,
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 7_1_2 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) Version/7.0 Mobile/11D257 Safari/9537.53",
        }
        self.session = requests.Session()

    def get_images(self, search_text: str) -> dict:
        url = "https://api.freepik.com/v1/resources"
        params = {
            "locale": "en-US",
            "page": 1,
            "limit": 5,
            "order": "latest",
            "term":search_text,
        }

        response = requests.get(url, params=params, headers=self.headers)

        if response.status_code == 200:
            response_data = response.json()
            pictures = response_data["data"]

            if pictures:
                data = {pic["image"]["source"]["url"] for pic in pictures}

                return {
                    f"image_{index + 35}": picture
                    for index, picture in enumerate(data)
                }

