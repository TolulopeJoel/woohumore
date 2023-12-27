from django.urls import path

from . import views

urlpatterns = [
    path(
        'subscribe/', views.SubscriberCreateView.as_view(), name='subscribers-create'
    ),
    path(
        'subscribers/', views.SubscriberListView.as_view(), name='subscribers-list'
    ),
]
