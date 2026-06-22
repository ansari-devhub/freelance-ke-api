from rest_framework.viewsets import ModelViewSet
from apps.bookings.models import Booking
from apps.bookings.serializers import BookingSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from core.permissions import IsClient, IsBookingParticipant
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class BookingViewSet(ModelViewSet):
    queryset = Booking.objects.select_related('client__user', 'service__freelancer__user')
    serializer_class = BookingSerializer
    filterset_fields = ['status']
    search_fields = ['service__title', 'client__user__email']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    
    @action(detail=True, methods=['post'], url_path='cancel')
    def cancel(self, request, pk=None):
        booking = self.get_object()
        if booking.status == Booking.Status.COMPLETED:
            return Response(
                {'error': 'Cannot cancel a completed booking'},
                status=status.HTTP_400_BAD_REQUEST
            )
        booking.status = Booking.Status.CANCELLED
        booking.save()
        return Response({'status': 'booking cancelled'})
    
    def perform_create(self, serializer):
        client_profile = self.request.user.client_user
        serializer.save(client=client_profile)
            
    def get_permissions(self):
        if self.action == 'create':
            return [IsClient()]
        if self.action in ['retrieve', 'cancel']:
            return [IsBookingParticipant()]
        return [IsAuthenticated()]