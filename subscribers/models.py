from django.db import models


class Subscriber(models.Model):
    email = models.CharField(max_length=225)
    verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
