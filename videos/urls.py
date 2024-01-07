from django.urls import path
from . import views

urlpatterns = [
    path('create-audio/', views.CreatePostAudio.as_view(), name='create-audio'),
]