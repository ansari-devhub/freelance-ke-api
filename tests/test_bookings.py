from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from apps.accounts.models import User, FreelancerProfile, ClientProfile
from apps.services.models import Service
from apps.bookings.models import Booking

class BookingTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
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
        self.client.force_authenticate(user=self.client_user)

    def test_create_booking(self):
        response = self.client.post('/api/bookings/', {
            'service_id': self.service.id,
            'note': 'I need a logo'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_cancel_booking(self):
        booking = Booking.objects.create(
            client=self.client_profile,
            service=self.service,
            status=Booking.Status.PENDING
        )
        response = self.client.post(f'/api/bookings/{booking.id}/cancel/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        booking.refresh_from_db()
        self.assertEqual(booking.status, Booking.Status.CANCELLED)

    def test_cannot_cancel_completed_booking(self):
        booking = Booking.objects.create(
            client=self.client_profile,
            service=self.service,
            status=Booking.Status.COMPLETED
        )
        response = self.client.post(f'/api/bookings/{booking.id}/cancel/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_freelancer_cannot_create_booking(self):
        self.client.force_authenticate(user=self.freelancer_user)
        response = self.client.post('/api/bookings/', {
            'service_id': self.service.id,
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)