from django.contrib import admin
from .models import FreelancerProfile, User, ClientProfile, Skill

# Register your models here.

admin.site.register(FreelancerProfile)
admin.site.register(ClientProfile)
admin.site.register(Skill)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'username', 'role', 'is_active']
    list_filter = ['role', 'is_active']
    search_fields = ['email', 'username']