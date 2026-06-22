from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Booking
from apps.notifications.models import Notification

@receiver(post_save, sender=Booking)
def booking_created_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user = instance.service.freelancer.user ,
            message = f"New booking for {instance.service.title} from {instance.client.user.email}"
        )
        Notification.objects.create(
            user = instance.client.user,
            message = f"Your booking for {instance.service.title} has been placed successfully"
        )