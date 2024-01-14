from io import BytesIO

import numpy as np
import requests
from django.conf import settings
from moviepy.editor import ImageSequenceClip, concatenate_videoclips
from PIL import Image
import cloudinary


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
    final_video.write_videofile(video_path, codec='libx264')
    video_data = cloudinary.uploader.upload(video_path)  # upload video

    return video_data["secure_url"]


def create_video_clips(images: list, audio_length: float):
    """
    Create video from a post.
    """
    image_files = [
        np.array(Image.open(BytesIO(requests.get(post).content))
                 .resize((1440, 1080), Image.Resampling.LANCZOS))
        for post in images
    ]
    duration = audio_length / len(image_files)
    fps = 1 / duration

    return ImageSequenceClip(image_files, fps=fps)
