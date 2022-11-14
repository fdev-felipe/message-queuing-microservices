from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

CREATE_STOCK_URL = reverse('stock')

class StockApiTests(TestCase):
    """Test the stock endpoint"""

    def SetUp(self):
        self.client = APIClient()

    def test_stock_without_token(self):
        """Test access stock without token"""
        url = CREATE_STOCK_URL + '?q=ma.us'
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(res.data, {"detail": "Authentication credentials were not provided."})

    def test_stock_with_token(self):
        """Test access stock with token"""
        pass
