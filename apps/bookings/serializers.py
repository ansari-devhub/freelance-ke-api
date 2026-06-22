from rest_framework import serializers
from apps.accounts.models import ClientProfile
from apps.services.models import Service
from apps.services.serializers import ServiceSerializer
from .models import Booking
from apps.accounts.serializers import ClientProfileSerializer

class BookingSerializer(serializers.ModelSerializer):
    client = ClientProfileSerializer(read_only=True)
    service =  ServiceSerializer(read_only=True)
    # client_id = serializers.PrimaryKeyRelatedField(
    #     queryset=ClientProfile.objects.all(),
    #     source='client',
    #     write_only=True
    # )
    service_id = serializers.PrimaryKeyRelatedField(
        queryset=Service.objects.all(),
        source='service',
        write_only=True
    )
    class Meta:
        model = Booking
        fields = [
            'id',
            'client',
            'service',
            'status',
            'note',
            'created_at',
            # 'client_id',
            'service_id'
        ]
        read_only_fields = [
            'status'
        ]