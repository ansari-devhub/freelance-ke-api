from django.contrib import admin
from .models import Service, ServiceImage

# Register your models here.
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'freelancer', 'category', 'price', 'is_active']
    list_filter = ['category', 'is_active']
    search_fields = ['title', 'description']
    
    
admin.site.register(ServiceImage)