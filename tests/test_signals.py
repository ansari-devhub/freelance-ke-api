from rest_framework.test import APITestCase
from apps.accounts.models import User, FreelancerProfile, ClientProfile
from apps.services.models import Service
from apps.bookings.models import Booking
from apps.notifications.models import Notification

class SignalTestCase(APITestCase):
    def setUp(self):
        self.freelancer_user = User.objects.create_user(
            username='freelancer',
            email='freelancer@test.com',
            password='pass123',
            role='freelancer'
        )
        self.freelancer_profile = FreelancerProfile.objects.create(
            user=self.freelancer_user
        )
        self.client_user = User.objects.create_user(
            username='client',
            email='client@test.com',
            password='pass123',
            role='client'
        )
        self.client_profile = ClientProfile.objects.create(
            user=self.client_user
        )
        self.service = Service.objects.create(
            freelancer=self.freelancer_profile,
            title='Logo Design',
            description='Logo work',
            category='design',
            price=5000,
            delivery_days=3
        )

    def test_booking_creates_notifications(self):
        Booking.objects.create(
            client=self.client_profile,
            service=self.service
        )
        self.assertEqual(Notification.objects.count(), 2)

    def test_freelancer_gets_notified(self):
        Booking.objects.create(
            client=self.client_profile,
            service=self.service
        )
        self.assertTrue(
            Notification.objects.filter(
                user=self.freelancer_user
            ).exists()
        )

    def test_client_gets_notified(self):
        Booking.objects.create(
            client=self.client_profile,
            service=self.service
        )
        self.assertTrue(
            Notification.objects.filter(
                user=self.client_user
            ).exists()
        )