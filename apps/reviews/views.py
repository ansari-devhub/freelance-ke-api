from rest_framework.viewsets import ModelViewSet
from apps.reviews.models import Review
from apps.reviews.serializers import ReviewSerializer

# Create your views here.
class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.select_related('booking__client__user', 'booking__service')
    serializer_class = ReviewSerializer
    filterset_fields = ['rating']
    ordering_fields = ['rating', 'created_at']
    ordering = ['-created_at']
    search_fields = ['comment', 'booking__service__title']