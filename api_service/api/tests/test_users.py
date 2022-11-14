from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model


CREATE_USER_URL = reverse('user_create')
LOGIN_USER_URL = reverse('login')
LOGOUT_USER_URL = reverse('logout')

class UserApiTests(TestCase):
    """Test the users API"""

    def SetUp(self):
        self.client = APIClient()


    def test_create_valid_user_successful(self):
        """Test creating user with valid payload is successful"""

        payload = {
                "first_name": "Felipe",
                "last_name": "Sá",
                "email": "felipe@gmail.com",
                "password": "1234",
                "password_confirm": "1234"
            }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertNotIn('password', res.data)


    def test_password_does_not_match(self):
        """Test creating user when password does not match"""

        payload = {
            "first_name": "Felipe",
            "last_name": "Sá",
            "email": "felipe@gmail.com",
            "password": "1234",
            "password_confirm": "123445"
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(res.data, {"detail": "Password does not match"})


    def test_create_valid_superuser_successful(self):
        """Test creating super user with valid payload is successful"""

        payload = {
            "first_name": "Felipe",
            "last_name": "Sá",
            "email": "felipe@gmail.com",
            "password": "1234",
            "password_confirm": "1234",
            "is_superuser": True
        }

        result = {
            "id": 1,
            "first_name": "Felipe",
            "last_name": "Sá",
            "email": "felipe@gmail.com",
            "is_superuser": True
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertNotIn('password', res.data)
        self.assertEqual(res.data, result)


    def test_user_exists(self):
        """Test creating user that already exists"""

        payload = {
            "first_name": "Felipe",
            "last_name": "Sá",
            "email": "felipe@gmail.com",
            "password": "1234",
            "is_superuser": True
        }

        payload2 = {
            "first_name": "Felipe",
            "last_name": "Sá",
            "email": "felipe@gmail.com",
            "password": "1234",
            "password_confirm": "1234",
            "is_superuser": True
        }

        user = get_user_model().objects.create(**payload)
        self.assertEqual(user.email, payload['email'])
        res = self.client.post(CREATE_USER_URL, payload2)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data, {"email": ["user with this email already exists."]})


    def test_login_user_not_registred(self):
        """Test login with user does not registred"""

        payload = {
            "email": "felipe@gmail.com",
            "password": "1234"
        }

        res = self.client.post(LOGIN_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(res.data, {"detail": "User not found!"})


    def test_login_using_get(self):
        """Test login using get"""

        payload = {
            "email": "felipe@gmail.com",
            "password": "1234"
        }

        res = self.client.get(LOGIN_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


    def test_login_successful(self):
        """Test login with email successful"""
        pass

    def test_logout(self):
        """Test deleting token from cookie"""
        pass



