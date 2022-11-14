from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

CREATE_STATS_URL = reverse('stats')

class HistoryApiTests(TestCase):
    """Test the stats endpoint"""

    def SetUp(self):
        self.client = APIClient()

    def test_stats_without_token(self):
        """Test access stats without token"""
        url = CREATE_STATS_URL
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(res.data, {"detail": "Authentication credentials were not provided."})


    def test_stats_with_token_not_superuser(self):
        """Test access stats with token but user is not superuser"""
        pass

    def test_stats_with_token_superuser(self):
        """Test access stats with token and user is superuser"""
        pass
