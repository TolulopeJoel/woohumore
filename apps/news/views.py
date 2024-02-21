from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.views import Response, status

from apps.posts.models import Post

from utils.video import create_news_video

from .models import News
from .serializers import NewsSerializer


class NewsListAPIView(ListAPIView):
    queryset = News.objects.filter(is_published=True)
    serializer_class = NewsSerializer


class NewsCreateView(GenericAPIView):
    """
    A view to create a video from a batch of posts.
    """
    serializer_class = NewsSerializer
    queryset = Post.objects.filter(
        has_audio=True,
        has_video=False,
        is_published=False
    )[:5]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if queryset := self.get_queryset():
            news = News.objects.create(title=queryset.first().title)
            news.posts.set(queryset)
            news.video = create_news_video(queryset, news.id)
            news.save()

            # TODO: algortithm to publish news

            return Response(
                {
                    "status": "success",
                    **serializer.data
                },
                status=status.HTTP_201_CREATED
            )

        return Response({'status': 'failed'}, status=status.HTTP_400_BAD_REQUEST)
