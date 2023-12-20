from rest_framework import generics, viewsets

from .models import NewsSource, Post
from .serializers import (
    NewsSourceDetailSerializer,
    NewsSourceSerializer,
    PostSerializer,
    PublicPostSerializer
)


class NewsSourceViewset(viewsets.ReadOnlyModelViewSet):
    queryset = NewsSource.objects.all()
    serializer_class = NewsSourceSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return NewsSourceDetailSerializer
        return super().get_serializer_class()


class PostViewset(viewsets.ReadOnlyModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_serializer_class(self):
        user = self.request.user

        # return public serializer for Anonymous users
        if not user.is_superuser:
            return PublicPostSerializer

        return super().get_serializer_class()

    def get_queryset(self):
        default_queryset = super().get_queryset()

        # return queryset with only published posts for Anonymous users
        if self.get_serializer_class() == PublicPostSerializer:
            return default_queryset.filter(validated=True, published=True)

        return default_queryset
