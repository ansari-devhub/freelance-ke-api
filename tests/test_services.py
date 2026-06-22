from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from apps.accounts.models import User, FreelancerProfile, ClientProfile
from apps.services.models import Service

class ServiceCRUDTestCase(APITestCase):
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
        self.service_data = {
            'title': 'Logo Design',
            'description': 'Professional logo design',
            'category': 'design',
            'price': '5000.00',
            'delivery_days': 3,
        }
        self.client.force_authenticate(user=self.freelancer_user)

    def test_create_service_as_freelancer(self):
        response = self.client.post('/api/services/', self.service_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_service_as_client(self):
        self.client.force_authenticate(user=self.client_user)
        response = self.client.post('/api/services/', self.service_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_services(self):
        response = self.client.get('/api/services/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_by_category(self):
        Service.objects.create(
            freelancer=self.freelancer_profile,
            title='Logo Design',
            description='Logo',
            category='design',
            price=5000,
            delivery_days=3
        )
        Service.objects.create(
            freelancer=self.freelancer_profile,
            title='Blog Post',
            description='Writing',
            category='writing',
            price=2000,
            delivery_days=2
        )
        response = self.client.get('/api/services/?category=design')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_search_by_title(self):
        Service.objects.create(
            freelancer=self.freelancer_profile,
            title='Logo Design',
            description='Logo work',
            category='design',
            price=5000,
            delivery_days=3
        )
        response = self.client.get('/api/services/?search=Logo')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_toggle_availability(self):
        service = Service.objects.create(
            freelancer=self.freelancer_profile,
            title='Logo Design',
            description='Logo work',
            category='design',
            price=5000,
            delivery_days=3
        )
        original = service.is_active
        response = self.client.post(
            f'/api/services/{service.id}/toggle-availability/'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['is_active'], not original)