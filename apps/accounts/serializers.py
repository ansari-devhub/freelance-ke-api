from rest_framework import serializers
from .models import Skill, User, FreelancerProfile, ClientProfile

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name']
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        read_only_fields = ['role']
        fields = [
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'role',
            'phone_number',
            'location'
        ]
        
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'username',
            'password',
            'role'
        ]
        
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user 
    
class FreelancerProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only = True)
    skills = SkillSerializer(many = True, read_only = True)
    class Meta:
        model = FreelancerProfile
        fields = [
            'id',
            'user',
            'bio',
            'hourly_rate',
            'is_available',
            'skills'
        ]
        
class ClientProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only = True)
    class Meta:
        model = ClientProfile
        fields = [
            'id',
            'user',
            'company_name'
        ]