from rest_framework.viewsets import ModelViewSet
from apps.notifications.models import Notification
from apps.notifications.serializers import NotificationSerializer
from rest_framework.response import Response
from rest_framework.decorators import action

from core.permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class NotificationViewSet(ModelViewSet):
    queryset = Notification.objects.select_related('user')
    serializer_class = NotificationSerializer
    filterset_fields = ['is_read']
    ordering = ['-created_at']
    
    @action(detail=True, methods=['post'], url_path='mark-read')
    def mark_read(self, request, pk=None):
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        return Response({'is_read': True})
    
    def get_permissions(self):
        if self.action == 'mark_read':
            return [IsOwnerOrReadOnly()]
        return [IsAuthenticated()]