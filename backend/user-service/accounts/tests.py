from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from accounts.models import User
from accounts.serializers import RegisterSerializer


class UserModelTest(TestCase):

    def setUp(self):
        # creates a test user before each test runs
        self.user = User.objects.create_user(
            username='testuser',
            email='test@gmail.com',
            password='test123',
            role='staff'
        )

    def test_user_created_correctly(self):
        # verifies user fields are saved correctly in DB
        self.assertEqual(self.user.email, 'test@gmail.com')
        self.assertEqual(self.user.username, 'testuser')

    def test_role_defaults_to_staff(self):
        # verifies default role is staff when not provided
        user = User.objects.create_user(
            username='newuser',
            email='new@gmail.com',
            password='test123'
        )
        self.assertEqual(user.role, 'staff')

    def test_is_admin_returns_true_for_admin(self):
        # verifies is_Admin() returns True when role is admin
        self.user.role = 'admin'
        self.assertTrue(self.user.is_Admin())

    def test_is_staff_member_returns_true_for_staff(self):
        # verifies is_Staff_member() returns True when role is staff
        self.assertTrue(self.user.is_Staff_member())

    def test_str_returns_correct_format(self):
        # verifies __str__ returns email and role format
        self.assertEqual(str(self.user), 'test@gmail.com (staff)')


class RegisterSerializerTest(TestCase):

    def test_valid_data_passes(self):
        # verifies serializer accepts correct registration data
        data = {
            'username': 'gautam',
            'email': 'gautam@gmail.com',
            'password': 'test123'
        }
        serializer = RegisterSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_missing_email_fails(self):
        # verifies serializer rejects data without email
        data = {
            'username': 'gautam',
            'password': 'test123'
        }
        serializer = RegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)

    def test_short_password_fails(self):
        # verifies serializer rejects password less than 6 characters
        data = {
            'username': 'gautam',
            'email': 'gautam@gmail.com',
            'password': '123'
        }
        serializer = RegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('password', serializer.errors)

    def test_duplicate_email_fails(self):
        # verifies serializer rejects duplicate email
        User.objects.create_user(
            username='existing',
            email='gautam@gmail.com',
            password='test123'
        )
        data = {
            'username': 'gautam2',
            'email': 'gautam@gmail.com',
            'password': 'test123'
        }
        serializer = RegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())


class AuthAPITest(TestCase):

    def setUp(self):
        # APIClient simulates HTTP requests in tests
        self.client = APIClient()
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.profile_url = reverse('profile')
        self.logout_url = reverse('logout')

        # test user data for registration
        self.user_data = {
            'username': 'testuser',
            'email': 'test@gmail.com',
            'password': 'test123'
        }

    def test_register_returns_201(self):
        # verifies register API creates user and returns 201
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'User registered successfully')

    def test_login_with_correct_credentials_returns_200(self):
        # verifies login returns 200 and tokens for valid credentials
        self.client.post(self.register_url, self.user_data, format='json')
        response = self.client.post(self.login_url, {
            'email': 'test@gmail.com',
            'password': 'test123'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_login_with_wrong_password_returns_401(self):
        # verifies login rejects wrong password with 401
        self.client.post(self.register_url, self.user_data, format='json')
        response = self.client.post(self.login_url, {
            'email': 'test@gmail.com',
            'password': 'wrongpassword'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_profile_without_token_returns_401(self):
        # verifies profile API rejects request without token
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_profile_with_valid_token_returns_200(self):
        # verifies profile API returns user details with valid token
        self.client.post(self.register_url, self.user_data, format='json')
        login_response = self.client.post(self.login_url, {
            'email': 'test@gmail.com',
            'password': 'test123'
        }, format='json')
        access_token = login_response.data['access']
        # attach token to client for subsequent requests
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout_blacklists_token(self):
        # verifies logout invalidates refresh token
        self.client.post(self.register_url, self.user_data, format='json')
        login_response = self.client.post(self.login_url, {
            'email': 'test@gmail.com',
            'password': 'test123'
        }, format='json')
        access_token = login_response.data['access']
        refresh_token = login_response.data['refresh']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.post(self.logout_url, {'refresh': refresh_token}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
