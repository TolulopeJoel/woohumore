from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from .models import Post, Source


class BaseAPITestCase(APITestCase):
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
            link_to_news="https://example.com/odd/example-post2",
        )

        self.published_post = Post.objects.create(
            news_source=self.source,
            title="Example Post",
            body="Example body",
            link_to_news="https://example.com/odd/example-post",
            is_published=True,
            has_body=True,
        )


class SourceViewsetTest(BaseAPITestCase):
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


class PostTest(BaseAPITestCase):
    def test_published_post_list(self):
        """
        Tests that all listed posts are published posts
        """
        endpoint = reverse('posts-list')
        response = self.client.get(endpoint)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.data),
            Post.objects.filter(is_published=True).count()
        )

    def test_published_post_bodied_post(self):
        """
        Tests that only posts with a body are published
        """
        endpoint = reverse('posts-list')
        response = self.client.get(endpoint)

        for post_data in response.data:
            post = Post.objects.get(id=post_data['id'])
            self.assertTrue(post.has_body)

    def test_published_post_published_date(self):
        """
        Tests that published posts have a published date
        """
        endpoint = reverse('posts-list')
        response = self.client.get(endpoint)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for post_data in response.data:
            post = Post.objects.get(id=post_data['id'])
            self.assertIsNotNone(post.published_date)

    def test_published_post_body(self):
        """
        Tests that published posts have a valid body
        """
        endpoint = reverse('posts-list')
        response = self.client.get(endpoint)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for post_data in response.data:
            post = Post.objects.get(id=post_data['id'])
            self.assertTrue(post.body)
            self.assertNotEqual(post.body, "None")

    def test_unpublished_post_published_date(self):
        """
        Tests that unpublished posts don't have a published date
        """
        unpublished_posts = Post.objects.filter(is_published=False)

        for post in unpublished_posts:
            self.assertIsNone(post.published_date)

    def test_auto_update_published_date(self):
        """
        Tests that the published_date is automatically updated
        when a post is saved and published
        """
        self.post.is_published = True
        self.post.save()

        self.assertIsNotNone(self.post.published_date)

    def test_ordering_of_posts(self):
        """
        Tests that the posts are ordered by created_at field
        """
        endpoint = reverse('posts-list')
        response = self.client.get(endpoint)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        posts = Post.objects.filter(is_published=True).order_by('-created_at')
        for i, post_data in enumerate(response.data):
            post = posts[i]
            self.assertEqual(post_data['id'], post.id)

    def test_unique_link_per_post(self):
        """
        Tests that post link is unique
        """
        new_post = Post(
            news_source=self.source,
            title="Example Post",
            body="Another body",
            link_to_news="https://example.com/odd/example-post",
            is_published=True,
            published_date="2024-01-05T12:00:00Z"
        )
        with self.assertRaises(IntegrityError):
            new_post.save()


class SummaryTest(BaseAPITestCase):
    def test_summarize_posts_no_new_posts(self):
        self.published_post.is_summarised = True
        self.published_post.save()

        url = reverse('summarise-posts')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'success')
        self.assertEqual(response.data['message'], 'No new posts')

    def test_summarize_posts_success(self):
        url = reverse('summarise-posts')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'success')
        self.assertEqual(response.data['message'],
                         '1 posts have been added sucessfully')
