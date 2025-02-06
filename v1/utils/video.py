import os
from io import BytesIO

import cloudinary
import numpy as np
import requests
from django.conf import settings
from moviepy.editor import (AudioFileClip, ImageSequenceClip,
                            concatenate_videoclips)
from PIL import Image

from apps.posts.models import Post


def create_news_video(posts: list[Post], news_id: str) -> str:
    """
    Joins video clips into one video, writes it to a file,
    and uploads it to a cloud storage service.
    """
    video_clips = create_video_clips(posts)
    final_video = concatenate_videoclips(video_clips, method="compose")
    video_path = f"{settings.MEDIA_VIDEOS_PATH}/{news_id}_final_video.mp4"
    final_video.write_videofile(video_path, codec='libx264', audio_codec='aac')
    video_data = cloudinary.uploader.upload(video_path, resource_type="video")

    # delete local video file after upload
    os.remove(video_path)

    return video_data["secure_url"]


def create_video_clips(posts: list[Post]) -> list[ImageSequenceClip]:
    video_clips = []
    for post in posts:
        video = _create_video_clip(post)
        post.has_video = True
        post.save()
        video_clips.append(video)

    return video_clips


def _create_video_clip(post: Post, size=(1440, 1080)) -> ImageSequenceClip:
    """
    Create video from a post.
    """
    image_files = [
        np.array(
            Image.open(BytesIO(requests.get(image).content))
            .resize(size, Image.Resampling.LANCZOS)
        )
        for image in post.images.values()
    ]
    duration = post.audio_length / len(image_files)
    fps = 1 / duration

    video_clip = ImageSequenceClip(image_files, fps=fps)
    video_clip = _add_audio_to_video_clip(
        post.id, video_clip, audio_url=post.audio)

    return video_clip


def _add_audio_to_video_clip(
    id: str,
    video_clip: ImageSequenceClip,
    audio_url: str = None,
    audio_path: str = None
) -> AudioFileClip:
    """
    Adds audio to a video clip.
    """

    if audio_url:
        audio_response = requests.get(audio_url)

        # Save the audio file
        audio_filename = f"{id}_downloaded_audio.wav"
        with open(audio_filename, "wb") as audio_file:
            audio_file.write(audio_response.content)

        # Load audio clip
        audio_clip = AudioFileClip(audio_filename)
        video_clip = video_clip.set_audio(audio_clip)

        # delete local audio file
        os.remove(audio_filename)

        return video_clip
