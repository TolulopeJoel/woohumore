from django.shortcuts import redirect
from django.urls import reverse
from rest_framework.generics import GenericAPIView

from apps.posts.models import Post
from apps.posts.views import SourceViewset
from utils.scraper import get_post_detail, get_post_list


class ScrapePostListView(GenericAPIView):
    """
    Returns list of new posts from the news sources.
    """
    new_posts_count = 0
    queryset = SourceViewset.get_queryset(SourceViewset)

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        get_post_list(queryset)

        return redirect(reverse('scrape-post-detail'))


class ScrapePostDetailView(GenericAPIView):
    """
    Updates the post object with body(content) & post images.
    """

    def get(self, request, *args, **kwargs):
        queryset = Post.objects.filter(has_body=False)
        for post in queryset:
            get_post_detail(post)

        return redirect(reverse('summarise-posts'))
