from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from .models import Post, Source


class GeneralTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()

        self.source = Source.objects.create(
            name="example",
            domain="https://example.com",
            news_page="https://example.com/odd",
            active=True,
            title_tag="h2",
            link_tag="span",
            link_tag_class="active-section",
            body_tag="div",
            body_tag_class="w-post",
            image_tag="figure",
            image_tag_class="post-image"
        )

        self.post = Post.objects.create(
            news_source=self.source,
            title="Example Post",
            body="Example body",
            link_to_news="https://example.com/odd/example-post",
        )


class SourceViewsetTest(GeneralTestCase):
    def test_source_list(self):
        endpoint = reverse('sources-list')
        response = self.client.get(endpoint)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Source.objects.count())

    def test_only_active_source(self):
        self.source.active = False
        self.source.save()

        endpoint = reverse('sources-list')
        response = self.client.get(endpoint)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

        self.source.active = True
        self.source.save()
