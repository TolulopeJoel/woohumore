import urllib.parse

import requests
from django.conf import settings


class UnsplashService:
    def __init__(self) -> None:
        self.headers = {
            "Authorization": f"Client-ID {settings.UNSPLASH_CLIENT_ID}",
        }
        self.session = requests.Session()

    def get_images(self, search_text):

        params = {
            "query": search_text,
            "content_filter": "high",
            "orientation": "landscape",
            "per_page": 5,
        }
        params = urllib.parse.urlencode(params)

        url = f"https://api.unsplash.com/search/photos?{params}"
        response = self.session.get(url, headers=self.headers)

        if response.status_code == 200:
            response_data = response.json()

            pictures = response_data["results"][1:4]
            data = {pic["links"]["download"] for pic in pictures}

            return {
                f"image_{index + 35}": picture
                for index, picture in enumerate(data)
            }
