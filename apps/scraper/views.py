from django.shortcuts import redirect
from django.urls import reverse
from rest_framework.generics import GenericAPIView
from rest_framework.views import Response, status

from apps.posts.models import Post
from apps.posts.serializers import PostListSerializer
from apps.posts.views import SourceViewset
from utils.scraper import get_post_detail, get_post_list


class ScrapePostListView(GenericAPIView):
    """
    Returns list of new posts from the news sources.
    """
    serializer_class = PostListSerializer
    queryset = SourceViewset.get_queryset(SourceViewset)

    def get_serializer(self, *args, **kwargs):
        return super().get_serializer(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        posts = get_post_list(queryset)

        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)


class ScrapePostDetailView(GenericAPIView):
    """
    Updates the post object with body(content) & post images.
    """
    queryset = Post.objects.filter(has_body=False)

    def get(self, request, *args, **kwargs):
        for post in self.get_queryset():
            get_post_detail(post)

        return redirect(reverse('summarise-posts'))
