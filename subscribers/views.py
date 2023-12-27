from rest_framework.views import Response
from rest_framework import generics
from rest_framework.permissions import AllowAny

from .models import Subscriber
from .serializers import SubscriberSerializer

class SubscriberListView(generics.ListAPIView):
    queryset = Subscriber.objects.all()
    serializer_class = SubscriberSerializer


class SubscriberCreateView(generics.CreateAPIView):
    queryset = Subscriber.objects.all()
    serializer_class = SubscriberSerializer
    permission_classes = [AllowAny]
