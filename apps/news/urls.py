from django.urls import path

from .views import NewsListAPIView, NewsCreateView

urlpatterns = [
    path('', NewsListAPIView.as_view(), name='news-list'),
    path('create/', NewsCreateView.as_view(), name='create-video'),
]
