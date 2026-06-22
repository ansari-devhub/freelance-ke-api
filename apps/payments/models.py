from django.db import models
from apps.bookings.models import Booking

# Create your models here.
class Payment(models.Model):
    class Method(models.TextChoices):
        MPESA = 'mpesa', 'M-Pesa'
        CARD = 'card', 'Card'
        CASH = 'cash', 'Cash'
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        PAID = 'paid', 'Paid'
        FAILED = 'failed', 'Failed'
        REFUNDED = 'refunded', 'Refunded' 
          
    booking = models.OneToOneField(Booking, related_name='payment', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=10, choices=Method.choices, default=Method.MPESA)
    status = models.CharField(max_length=8, choices=Status.choices, default=Status.PENDING)
    transaction_id = models.CharField(max_length=100, blank=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Payment for {self.booking} - {self.status}"
    