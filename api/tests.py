from rest_framework.test import (APITestCase,
                                 APIClient) 
from rest_framework import status
from datetime import date

import json

# Create your tests here.

class RecordListViewTest(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_record_list(self):
        result = self.client.get('http://127.0.0.1:8000/api/ledgers/')
                
        self.assertEqual(result.status_code, status.HTTP_200_OK)

        
        