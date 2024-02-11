import os

import cloudinary
from rest_framework.generics import GenericAPIView
from rest_framework.views import Response

from apps.news.models import News
from apps.posts.models import Post

from .utils import create_audio, create_video, create_video_clip


class CreatePostAudioView(GenericAPIView):
    queryset = Post.objects.filter(is_summarised=True, has_audio=False)

    def get(self, request, *args, **kwargs):
        for post in self.get_queryset():
            audio_data = create_audio(post.id, post.body)

            if "path" in audio_data:
                upload_data = cloudinary.uploader.upload(
                    audio_data["path"],
                    resource_type="auto",
                )
                post.audio = upload_data["secure_url"]
                # delete local audio file after upload
                os.remove(audio_data["path"])
            else:
                post.audio = audio_data["url"]

            post.audio_length = upload_data["duration"]
            post.has_audio = True
            post.save()

        return Response({"status": "success", "message": "Audio upload successful."})


class CreateNewsVideoView(GenericAPIView):
    queryset = Post.objects.filter(
        has_audio=True,
        has_video=False,
        is_published=False
    )[:5]

    def get(self, request, *args, **kwargs):
        news = News.objects.create(title=self.get_queryset().first().title)
        news.posts.set(self.get_queryset())

        video_clips = []
        for post in self.get_queryset():
            video = create_video_clip(post)
            post.has_video = True
            post.save()
            video_clips.append(video)

        news.video = create_video(video_clips, news.id)
        news.is_published = True
        news.save()

        return Response({"status": "success", "message": "News video created successfully"})
