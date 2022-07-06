"""
Testing if api returns correct results.
"""
from rest_framework.test import RequestsClient
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.test import APIRequestFactory
import requests

API_VDA_URL = reverse('vda-detail', args=['rs295'])


#  this test needs to be fixed
class APItest(TestCase):

    """Test VDA api"""
    def setUp(self):
        self.client = RequestsClient()

    def test_api(self):
        """Testing if api call returns correct disease"""
        res = self.client.get('http://localhost:9078/api/vda/variants/rs295/')
        print('res: ', res)
        # self.assertEqual(res.status_code, status.HTTP_200_OK)

