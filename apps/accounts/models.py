from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    class Role(models.TextChoices):
        FREELANCER = 'freelancer', 'Freelancer'
        CLIENT = 'client', 'Client'
        ADMIN = 'admin', 'Admin'
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    role = models.CharField(max_length=10, choices=Role, default=Role.FREELANCER)
    
    def __str__(self):
        return self.email
    
class Skill(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name

    
class FreelancerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='freelance_user')
    bio = models.TextField(blank=True, null=True)
    hourly_rate = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    is_available = models.BooleanField(default=True)
    skills = models.ManyToManyField(Skill, blank=True)
    
    def __str__(self):
        return f"{self.user.email} - Freelancer"
    
class ClientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='client_user')
    company_name = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.email} - Client"