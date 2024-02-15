import random

from django.conf import settings
from rest_framework.generics import GenericAPIView
from rest_framework.views import Response, status

from apps.news.models import News
from apps.posts.models import Post
from services.play import PlayAudioService
from utils.video import create_news_video


class CreatePostAudioView(GenericAPIView):
    # Only supports posts w/ images for now.
    queryset = (
        Post.objects
        .filter(is_summarised=True, has_audio=False)
        .exclude(images__exact={})
    )

    def get(self, request, *args, **kwargs):
        for post in self.get_queryset():
            play_ht = PlayAudioService()
            voice = random.choice(settings.PLAY_VOICE)

            post.audio = play_ht.create_audio(post.body, voice)
            post.audio_length = play_ht.audio_length
            post.has_audio = True
            post.save()

        return Response({"status": "success", "message": "Audio upload successful."})


class CreateNewsVideoView(GenericAPIView):
    """
    A view to create a video from a batch of posts.
    """
    queryset = Post.objects.filter(
        has_audio=True,
        has_video=False,
        is_published=False
    )[:5]

    def post(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        news = News.objects.create(title=queryset.first().title)
        news.posts.set(queryset)
        news.video = create_news_video(queryset, news.id)
        news.save()

        # TODO: algortithm to publish news

        return Response(
            {
                "status": "success",
                "id": news.id,
                "title": news.title,
                "video": news.video,
                "created_at": news.created_at
            },
            status=status.HTTP_201_CREATED
        )
