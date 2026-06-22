from rest_framework.viewsets import ModelViewSet
from apps.services.filters import ServiceFilter
from apps.services.models import Service, ServiceImage
from apps.services.serializers import ServiceImageSerializer, ServiceSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from core.pagination import ServiceCursorPagination
from core.permissions import IsFreelancer, IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

# Create your views here.
class ServiceViewSet(ModelViewSet):
    queryset = Service.objects.select_related('freelancer__user').prefetch_related('images')
    serializer_class = ServiceSerializer
    pagination_class = ServiceCursorPagination
    filterset_class = ServiceFilter
    search_fields = ['title', 'description']
    ordering_fields = ['price', 'created_at', 'delivery_days']
    ordering = ['-created_at']
    
    def perform_create(self, serializer):
        freelancer_profile = self.request.user.freelance_user
        serializer.save(freelancer=freelancer_profile)
    
    @action(detail=True, methods=['post'], url_path='toggle-availability')
    def toggle_availability(self, request, pk=None):
        service = self.get_object()
        service.is_active = not service.is_active
        service.save()
        return Response({'is_active': service.is_active})
    
    def get_permissions(self):
        if self.action in ['create']:
            return [IsFreelancer()]
        if self.action in ['update', 'partial_update', 'destroy', 'toggle_availability']:
            return [IsOwnerOrReadOnly()]
        return [IsAuthenticatedOrReadOnly()]
    
class ServiceImageViewSet(ModelViewSet):
    queryset = ServiceImage.objects.select_related('service')
    serializer_class = ServiceImageSerializer
    permission_classes = [IsAuthenticated]