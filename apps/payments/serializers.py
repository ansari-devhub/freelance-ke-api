from rest_framework import serializers
from apps.bookings.serializers import BookingSerializer
from .models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    booking = BookingSerializer(read_only=True)
    class Meta:
        model = Payment
        fields = [
            'id',
            'booking',
            'amount',
            'method',
            'status',
            'transaction_id',
            'paid_at',
            'created_at'
        ]
        read_only_fields = [
            'status',
            'transaction_id'
        ]