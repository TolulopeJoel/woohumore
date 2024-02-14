from django.urls import path

from .views import NewsListAPIView

urlpatterns = [
    path('', NewsListAPIView.as_view(), name='news-list')
]
