from django.db import models
from apps.accounts.models import FreelancerProfile

# Create your models here.
class Service(models.Model):
    class Category(models.TextChoices):
        DESIGN = 'design', 'Design'
        DEVELOPMENT = 'development', 'Development'
        WRITING = 'writing', 'Writing'
        PHOTOGRAPHY = 'photography', 'Photography'
        ERRANDS = 'errands', 'Errands'
        OTHER = 'other', 'Other'
    freelancer = models.ForeignKey(FreelancerProfile, on_delete=models.CASCADE ,related_name='services')
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=11, choices=Category.choices)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    delivery_days = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
class ServiceImage(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='service_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Image for {self.service.title}"
    
    