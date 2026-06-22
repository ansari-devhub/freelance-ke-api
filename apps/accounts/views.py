from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from apps.accounts.models import ClientProfile, FreelancerProfile, Skill
from apps.accounts.serializers import ClientProfileSerializer, FreelancerProfileSerializer, RegisterSerializer, SkillSerializer
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from django.db.models import Sum, Count

from core.permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class SkillViewSet(ReadOnlyModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [AllowAny]
    
class FreelancerProfileViewSet(ModelViewSet):
    queryset = FreelancerProfile.objects.select_related('user').prefetch_related('skills')
    serializer_class = FreelancerProfileSerializer
    filterset_fields = ['is_available']
    search_fields = ['user__email', 'user__location', 'skills__name']
    ordering_fields = ['hourly_rate']
    ordering = ['-user__date_joined']  # newest freelancers first
    
    @action(detail=True, methods=['get'], url_path='earnings-summary')
    def earnings_summary(self, request, pk=None):
        freelancer = self.get_object()
        data = freelancer.services.aggregate(
        total_services=Count('id'),
        total_earnings=Sum('bookings__payment__amount')
        )
        data['total_earnings'] = data['total_earnings'] or 0
        return Response(data)
    
    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsOwnerOrReadOnly()]
        return [IsAuthenticated()]
    
class ClientProfileViewSet(ModelViewSet):
    queryset = ClientProfile.objects.select_related('user')
    serializer_class = ClientProfileSerializer
    search_fields = ['user__email', 'company_name']
    
    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsOwnerOrReadOnly()]
        return [IsAuthenticated()]
    
    
class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]