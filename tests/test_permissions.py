from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from apps.accounts.models import User, FreelancerProfile
from apps.services.models import Service

class PermissionTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.freelancer_user_1 = User.objects.create_user(
            username='freelancer1',
            email='freelancer1@test.com',
            password='pass123',
            role='freelancer'
        )
        self.freelancer_profile_1 = FreelancerProfile.objects.create(
            user=self.freelancer_user_1
        )
        self.freelancer_user_2 = User.objects.create_user(
            username='freelancer2',
            email='freelancer2@test.com',
            password='pass123',
            role='freelancer'
        )
        self.freelancer_profile_2 = FreelancerProfile.objects.create(
            user=self.freelancer_user_2
        )
        self.service = Service.objects.create(
            freelancer=self.freelancer_profile_1,
            title='Logo Design',
            description='Logo work',
            category='design',
            price=5000,
            delivery_days=3
        )

    def test_owner_can_update_service(self):
        self.client.force_authenticate(user=self.freelancer_user_1)
        response = self.client.patch(
            f'/api/services/{self.service.id}/',
            {'title': 'Updated Logo Design'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_non_owner_cannot_update_service(self):
        self.client.force_authenticate(user=self.freelancer_user_2)
        response = self.client.patch(
            f'/api/services/{self.service.id}/',
            {'title': 'Hacked Title'}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated_cannot_create_service(self):
        response = self.client.post('/api/services/', {
            'title': 'Logo Design',
            'category': 'design',
            'price': 5000,
            'delivery_days': 3
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)