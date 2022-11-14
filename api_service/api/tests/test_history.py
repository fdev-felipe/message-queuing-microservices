from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

CREATE_HISTORY_URL = reverse('history')

class HistoryApiTests(TestCase):
    """Test the history endpoint"""

    def SetUp(self):
        self.client = APIClient()

    def test_history_without_token(self):
        """Test access history without token"""
        url = CREATE_HISTORY_URL
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(res.data, {"detail": "Authentication credentials were not provided."})


    def test_history_with_token(self):
        """Test access history with token"""
        pass
