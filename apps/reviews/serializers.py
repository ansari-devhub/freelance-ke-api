from rest_framework import serializers
from apps.bookings.serializers import BookingSerializer
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    booking = BookingSerializer(read_only=True)
    class Meta:
        model = Review
        fields = [
            'id',
            'booking',
            'rating',
            'comment',
            'created_at'
        ]
        
    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5")
        return value