from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register('posts', views.PostViewset, basename='posts')
router.register('sources', views.SourceViewset, basename='sources')


urlpatterns = [
    path('summarise-posts/', views.SummarisePostView.as_view(), name='summarise-posts')
]

urlpatterns += router.urls
