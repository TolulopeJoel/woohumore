import os
from io import BytesIO

import cloudinary
import numpy as np
import requests
from django.conf import settings
from moviepy.editor import AudioFileClip, ImageSequenceClip, concatenate_videoclips
from PIL import Image


def create_video(video_clips, news_id):
    """
    Joins video clips into one video, writes it to a file,
    and uploads it to a cloud storage service.

    Args:
        video_clips (list): A list of video clips to be joined.
        news_id (str): The ID of the news associated with the video.

    Returns:
        str: The secure URL of the uploaded video.

    """
    final_video = concatenate_videoclips(video_clips, method="compose")
    video_path = f"{settings.MEDIA_VIDEOS_PATH}/{news_id}_final_video.mp4"
    final_video.write_videofile(video_path, codec='libx264', audio_codec='aac')
    video_data = cloudinary.uploader.upload(video_path, resource_type="video")

    return video_data["secure_url"]


def create_video_clip(post, size=(1440, 1080)):
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


def _add_audio_to_video_clip(id, video_clip, audio_url=None, audio_path=None):
    """
    Adds audio to a video clip.

    Args:
        id (str): The ID of the video clip.
        video_clip (VideoClip): The video clip to which the audio will be added.
        audio_url (str, optional): The URL of the audio file to be added.
        audio_path (str, optional): The local path of the audio file to be added.

    Returns:
        VideoClip: The video clip with the added audio.
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
