from rest_framework import serializers
from apps.accounts.serializers import UserSerializer
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Notification
        fields = [
            'id',
            'user',
            'message',
            'is_read',
            'created_at'
        ]
        read_only_fields = [
            'message'
        ]
        