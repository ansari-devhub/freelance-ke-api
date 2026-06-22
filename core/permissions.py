from rest_framework.permissions import SAFE_METHODS, BasePermission

class IsFreelancer(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role == 'freelancer'
        )
        
class IsClient(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role == 'client'
        ) 
        
class IsOwnerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if hasattr(obj, 'user'):
            return obj.user == request.user
        if hasattr(obj, 'freelancer'):
            return obj.freelancer.user == request.user
        return False
    
class IsBookingParticipant(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        user = request.user
        is_client = obj.client.user == user
        is_freelancer = obj.service.freelancer.user == user
        return is_client or is_freelancer