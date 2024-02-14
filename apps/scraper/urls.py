from django.urls import path

from . import views

urlpatterns = [
    path('posts-list/', views.ScrapePostListView.as_view(), name='scrape-post-list'),
    path('posts-detail/', views.ScrapePostDetailView.as_view(), name='scrape-post-detail'),
]
