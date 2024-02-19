import random

from django.conf import settings

from rest_framework.generics import GenericAPIView
from rest_framework.views import Response

from apps.posts.models import Post
from services.play import PlayAudioService


class CreatePostAudioView(GenericAPIView):
    # Only supports posts w/ images for now.
    queryset = (
        Post.objects
        .filter(is_summarised=True, has_audio=False)
        .exclude(images__exact={})
    )

    def post(self, request, *args, **kwargs):
        for post in self.get_queryset():
            play_ht = PlayAudioService()
            voice = random.choice(settings.PLAY_VOICE)

            post.audio = play_ht.create_audio(post.body, voice)
            post.audio_length = play_ht.audio_length
            post.has_audio = True
            post.save()

        return Response({"status": "success", "message": "Audio upload successful."})
