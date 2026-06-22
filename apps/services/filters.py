import django_filters
from .models import Service

class ServiceFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    category = django_filters.CharFilter(field_name='category', lookup_expr='exact')
    location = django_filters.CharFilter(
        field_name='freelancer__user__location',
        lookup_expr='icontains'
    )
    is_active = django_filters.BooleanFilter(field_name='is_active')
    
    class Meta:
        model = Service
        fields = ['category', 'is_active', 'min_price', 'max_price', 'location']