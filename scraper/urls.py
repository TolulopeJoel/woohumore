from django.urls import path

from . import views

urlpatterns = [
    path('fetch-posts/', views.ScrapePostsView.as_view())
]