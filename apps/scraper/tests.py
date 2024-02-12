from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from posts.models import Post, Source

class ScrapePostTests(APITestCase):

    def setUp(self):
        self.source = Source.objects.create(
            name='Example News',
            news_page='https://example.com/news',
            link_tag='a',
            link_tag_class='post-link',
            title_tag='h2',
            domain='https://example.com'
        )

    def test_scrape_post_list_view(self):
        """
        Test the scrape post list view.
        """
        url = reverse('scrape-post-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_scrape_post_detail_view(self):
        """
        Test the scrape post detail view.
        """
        post = Post.objects.create(
            news_source=self.source,
            title='Test Post',
            body='This is a test post.',
            link_to_news='https://example.com/test-post'
        )

        url = reverse('scrape-post-detail')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
