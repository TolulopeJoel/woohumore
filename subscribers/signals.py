from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings

from .models import Subscriber


@receiver(post_save, sender=Subscriber)
def send_verification_email(sender, instance, **kwargs):
    """
    Signal handler to send verification email to a new subscriber.
    """
    subject = 'Verify your email'
    message = f'Your verification link: '
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [instance.email]
    send_mail(subject, message, from_email, recipient_list)
