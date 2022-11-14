# encoding: utf-8

from rest_framework.views import APIView

class StockView(APIView):
    """
    Receives stock requests from the API service.
    """
    def get(self, request,*args, **kwargs):
        # TODO: Make request to the stooq.com API, parse the response and send it to the API service.
        pass

"""Comunicating for message, not endpoint"""
