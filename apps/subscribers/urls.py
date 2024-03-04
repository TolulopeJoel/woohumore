from django.urls import path

from . import views

urlpatterns = [
    path(
        'add/', views.SubscriberCreateView.as_view(), name='subscribers-create'
    ),
    path(
        '', views.SubscriberListView.as_view(), name='subscribers-list'
    ),
]
