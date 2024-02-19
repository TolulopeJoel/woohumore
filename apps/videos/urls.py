from django.urls import path

from . import views

urlpatterns = [
    path('add-audio/', views.CreatePostAudioView.as_view(), name='create-audio'),
]
