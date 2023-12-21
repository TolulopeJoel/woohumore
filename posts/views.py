from rest_framework import viewsets

from .models import Post, Source
from .serializers import PostDetailSerializer, PostListSerializer, SourceSerializer


class SourceViewset(viewsets.ReadOnlyModelViewSet):
    queryset = Source.objects.filter(active=True)
    serializer_class = SourceSerializer


class PostViewset(viewsets.ReadOnlyModelViewSet):
    queryset = Post.objects.filter(published=True)
    serializer_class = PostListSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return PostDetailSerializer
        return super().get_serializer_class()
