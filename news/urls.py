from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

urlpatterns = [
    path('sources/', views.NewsSourceListView.as_view(), name='news_source_list'),
]

router = DefaultRouter()

router.register('posts', views.PostViewset, basename='posts')

urlpatterns += router.urls
