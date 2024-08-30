from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model


class UserAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(username='testuser', password='12345')
        self.client.force_authenticate(user=self.user)

    def test_login(self):
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': '12345'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout(self):
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_refresh_token(self):
        response = self.client.post(reverse('refresh'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_register(self):
        response = self.client.post(reverse('register'), {'username': 'newuser', 'password': '12345'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_detail(self):
        response = self.client.get(reverse('user-detail'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_async_routes(self):
        response = self.client.get(reverse('async-routes'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
