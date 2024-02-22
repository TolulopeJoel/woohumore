import urllib.parse

import requests
from django.conf import settings


class ShutterStockService:
    def __init__(self):
        self.headers = {
            "Authorization": f"Bearer {settings.SHUTTERSTOCK_API_TOKEN}",
        }
        self.session = requests.Session()

    def get_images(self, search_text: str) -> dict:
        params = {
            "query": search_text,
            "per_page": 5,
            "sort": "relevance",
        }
        params = urllib.parse.urlencode(params)
        url = f"https://api.shutterstock.com/v2/images/search?" + params

        response = self.session.get(url, headers=self.headers)
        print(response.status_code)

        if response.status_code == 200:
            response_data = response.json()

            pictures = response_data["data"][:4]
            data = {pic["assets"]["preview_1500"]["url"] for pic in pictures}

            return {
                f"image_{index + 35}": picture
                for index, picture in enumerate(data)
            }
