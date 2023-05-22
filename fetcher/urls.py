from django.urls import path

from . import views

urlpatterns = [
    path('fetch-posts/', views.ScrapeAndCountPostsView.as_view())
]