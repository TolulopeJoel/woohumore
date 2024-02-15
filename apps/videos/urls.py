from django.urls import path
from . import views

urlpatterns = [
    path('create/audio/', views.CreatePostAudioView.as_view(), name='create-audio'),
    path('create/video/', views.CreateNewsVideoView.as_view(), name='create-video'),
]
