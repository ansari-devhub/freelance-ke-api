from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.accounts.views import ClientProfileViewSet, FreelancerProfileViewSet, RegisterView, SkillViewSet
from apps.bookings.views import BookingViewSet
from apps.notifications.views import NotificationViewSet
from apps.payments.views import PaymentViewSet
from apps.reviews.views import ReviewViewSet
from apps.services.views import ServiceImageViewSet, ServiceViewSet

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register(r'skills', SkillViewSet, basename='skill')
router.register(r'freelancers', FreelancerProfileViewSet, basename='freelancer')
router.register(r'clients', ClientProfileViewSet, basename='client')
router.register(r'services', ServiceViewSet, basename='service')
router.register(r'service-images', ServiceImageViewSet, basename='service-image')
router.register(r'bookings', BookingViewSet, basename='booking')
router.register(r'payments', PaymentViewSet, basename='payment')
router.register(r'reviews', ReviewViewSet, basename='review')
router.register(r'notifications', NotificationViewSet, basename='notification')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/auth/register/', RegisterView.as_view(), name='register'),
    
    path('api/auth/login/', TokenObtainPairView.as_view(), name='login'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

