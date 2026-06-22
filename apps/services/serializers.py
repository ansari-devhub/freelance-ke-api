from rest_framework import serializers
from .models import Service, ServiceImage
from apps.accounts.serializers import FreelancerProfileSerializer

class ServiceImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceImage
        fields = [
            'id',
            'image',
            'uploaded_at'
        ]
        
class ServiceSerializer(serializers.ModelSerializer):
    freelancer = FreelancerProfileSerializer(read_only = True)
    images = ServiceImageSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()
    class Meta:
        model = Service
        fields = [
            'id',
            'freelancer',
            'title',
            'description',
            'category',
            'price',
            'delivery_days',
            'is_active',
            'created_at',
            'images',
            'average_rating'
        ]
        
    def get_average_rating(self, obj):
        from django.db.models import Avg
        return obj.bookings.filter(
            review__isnull=False
        ).aggregate(avg=Avg('review__rating'))['avg']