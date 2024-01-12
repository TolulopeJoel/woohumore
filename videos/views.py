import os
from io import BytesIO

import cloudinary
import numpy as np
import requests
from django.conf import settings
from moviepy.editor import ImageSequenceClip, concatenate_videoclips
from PIL import Image
from rest_framework.generics import GenericAPIView
from rest_framework.views import Response

from news.models import News
from posts.models import Post

from .utils import create_audio


class CreatePostAudioView(GenericAPIView):
    queryset = Post.objects.filter(is_summarised=True, has_audio=False)

    def get(self, request, *args, **kwargs):
        for post in self.get_queryset():
            file_path = create_audio(post.id, post.body)
            upload_data = cloudinary.uploader.upload(
                file_path,
                resource_type="auto",
            )

            post.audio = upload_data["secure_url"]
            post.audio_length = upload_data["duration"]
            post.has_audio = True
            post.save()
            # delete local audio file after upload
            os.remove(file_path)

        return Response({"status": "success", "message": "Audio upload successful."})

class CreateNewsVideoView(GenericAPIView):
    queryset = Post.objects.filter(
        has_audio=True,
        has_video=False,
        is_published=False
    )[:5]

    def get(self, request, *args, **kwargs):
        news = News.objects.create(
            title=self.get_queryset().first().title,
            posts=self.get_queryset(),
        )

        video_clips = []
        for post in self.get_queryset():
            video = self.create_video_clip(post)
            video_clips.append(video)

        # join video clips into one video
        final_video = concatenate_videoclips(video_clips, method="compose")
        video_path = f"{settings.MEDIA_VIDEOS_PATH}/{news.id}_final_video.mp4"
        final_video.write_videofile(video_path, codec='libx264')
        video_data = cloudinary.uploader.upload(video_path)  # upload video

        news.video = video_data["secure_url"]
        news.is_published = True
        news.save()

        return Response({"status": "success", "message": "News video created successfully"})

    def create_video_clip(self, post):
        """
        Create video from a post.

        Args:
            post: The post from which to create video from.

        Returns & Raises:
            None
        """

        image_files = [
            np.array(Image.open(BytesIO(requests.get(post).content))
                     .resize((1440, 1080), Image.Resampling.LANCZOS))
            for post in post.images.values()
        ]
        duration = post.audio_length / len(image_files)
        fps = 1 / duration

        return ImageSequenceClip(image_files, fps=fps)
