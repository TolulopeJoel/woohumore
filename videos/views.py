import os
import random
import wave
from io import BytesIO

import cloudinary
import numpy as np
import requests
from django.conf import settings
from moviepy.editor import ImageSequenceClip
from PIL import Image
from pyht import Client
from pyht.client import TTSOptions
from rest_framework.generics import GenericAPIView
from rest_framework.views import Response

from posts.models import Post


class CreatePostAudioView(GenericAPIView):
    queryset = Post.objects.filter(summarised=True, no_audio=True)

    def get(self, request, *args, **kwargs):
        for post in self.get_queryset():
            file_path = self.create_audio(post.id, post.body)
            upload_data = cloudinary.uploader.upload(
                file_path,
                resource_type="auto",
            )

            post.audio = upload_data["secure_url"]
            post.audio_length = upload_data["duration"]
            post.no_audio = False
            post.save()
            # delete local audio file after upload
            os.remove(file_path)

        return Response({"status": "success", "message": "Audio upload successful."})

    def create_audio(self, post_id, text):
        """
        Creates an audio file from the given text using a text-to-speech (TTS) client.

        Uses the specified `post_id` to generate a unique audio file path.
        Randomly selects a voice from the available options.
        Sets the TTS options with the chosen voice.

        Args:
            post_id: The ID of the post.
            text: The text (post body) to convert to audio.

        Returns:
            str: The path of the created audio file.
        """

        client = Client(
            user_id=settings.PLAY_USER_ID,
            api_key=settings.PLAY_API_KEY,
        )
        talker_voice = random.choice(settings.PLAY_VOICE)
        options = TTSOptions(voice=talker_voice)

        audio_file_path = f"{post_id}_output.wav"
        with wave.open(audio_file_path, 'w') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(24000)

            for chunk in client.tts(text, options):
                # convert chunk to bytes and write to the WAV file
                wf.writeframes(chunk)
            return audio_file_path

class CreateNewsVideoView(GenericAPIView):
    queryset = Post.objects.filter(no_audio=False)

    def get(self, request, *args, **kwargs):
        for post in self.get_queryset():
            video = self.create_video_chunks(post)

        return Response({"status": "success", "message": "News video created successfully"})

    def create_video_chunks(self, post):
        """
        Create video from a post.

        Args:
            post: The post from which to create video from.

        Returns & Raises:
            None
        """

        image_files = [
            np.array(Image.open(BytesIO(requests.get(post).content)))
            for post in post.images.values()
        ]
        duration = post.audio_length / len(image_files)
        fps = 1 / duration

        media_path = settings.MEDIA_URL
        output_file = f'{media_path}{post.id}_video.mp4'
        clip = ImageSequenceClip(image_files, fps=fps)
        # export video file
        clip.write_videofile(output_file, codec='libx264')
