from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from apps.accounts.models import User

class RegisterTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = '/api/auth/register/'
        self.valid_data = {
            'email': 'test@gmail.com',
            'username': 'testuser',
            'password': 'testpass123',
            'role': 'freelancer'
        }

    def test_register_success(self):
        response = self.client.post(self.url, self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)

    def test_register_duplicate_email(self):
        self.client.post(self.url, self.valid_data)
        response = self.client.post(self.url, self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_missing_password(self):
        data = self.valid_data.copy()
        data.pop('password')
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class LoginTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = '/api/auth/login/'
        self.user = User.objects.create_user(
            username='testuser',
            email='test@gmail.com',
            password='testpass123',
            role='freelancer'
        )

    def test_login_success(self):
        response = self.client.post(self.url, {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_login_wrong_password(self):
        response = self.client.post(self.url, {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)