from django.urls import path

from . import views

urlpatterns = [
    path('fetch-posts/', views.ScrapePostListView.as_view()),
    path('fetch-posts-detail/', views.ScrapePostDetailView.as_view())
]